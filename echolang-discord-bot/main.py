import discord
from discord.ext import commands
import asyncio
import logging
from translate import TranslationService
from languages import EMOJI_TO_LANGUAGE
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)
translation_service = TranslationService()

# Store active threads for cleanup
active_threads = {}
# Store thread deletion tasks for cancellation
thread_deletion_tasks = {}

@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    
    # List all guilds and their permissions
    for guild in bot.guilds:
        logger.info(f"Guild: {guild.name} (ID: {guild.id})")
        member = guild.get_member(bot.user.id)
        if member:
            logger.info(f"Bot permissions: {member.guild_permissions}")

@bot.event
async def on_raw_reaction_add(payload):
    """Handle raw reaction events"""
    logger.info(f"Raw reaction event: {payload.emoji} by user {payload.user_id}")
    
    # Skip bot's own reactions
    if payload.user_id == bot.user.id:
        return
    
    # Get the actual reaction and user objects
    channel = bot.get_channel(payload.channel_id)
    if not channel:
        logger.error(f"Channel {payload.channel_id} not found")
        return
        
    try:
        message = await channel.fetch_message(payload.message_id)
        
        # Try to get user with multiple methods
        user = None
        
        # Method 1: Guild member (works with members intent)
        if hasattr(channel, 'guild') and channel.guild:
            user = channel.guild.get_member(payload.user_id)
            if user:
                logger.info(f"Found user via guild member: {user.name}")
        
        # Method 2: Bot user cache
        if not user:
            user = bot.get_user(payload.user_id)
            if user:
                logger.info(f"Found user via bot cache: {user.name}")
        
        # Method 3: Fetch user directly
        if not user:
            try:
                user = await bot.fetch_user(payload.user_id)
                if user:
                    logger.info(f"Found user via fetch: {user.name}")
            except Exception as e:
                logger.error(f"Error fetching user: {e}")
        
        # Method 4: Create minimal user object as fallback
        if not user:
            class MinimalUser:
                def __init__(self, user_id):
                    self.id = user_id
                    self.name = f"User_{user_id}"
                    
            user = MinimalUser(payload.user_id)
            logger.info(f"Using fallback user object for {payload.user_id}")
            
        if not message:
            logger.error(f"Message {payload.message_id} not found")
            return
            
        logger.info(f"Processing reaction {payload.emoji} from user {user.name}")
        
        # Find the reaction object
        reaction_found = False
        for reaction in message.reactions:
            if str(reaction.emoji) == str(payload.emoji):
                logger.info(f"Found matching reaction, calling handler")
                await on_reaction_add(reaction, user)
                reaction_found = True
                break
                
        if not reaction_found:
            logger.error(f"Reaction {payload.emoji} not found in message reactions")
            
    except Exception as e:
        logger.error(f"Error in raw reaction handler: {e}")

@bot.event
async def on_reaction_add(reaction, user):
    """Handle emoji reactions added to messages"""
    logger.info(f"Reaction detected: {reaction.emoji} by {user.name}")
    
    # Ignore bot's own reactions
    if user.bot:
        logger.info(f"Ignoring bot reaction from {user.name}")
        return
    
    # Check if reaction is a flag emoji
    emoji_str = str(reaction.emoji)
    logger.info(f"Checking emoji: {emoji_str}")
    if emoji_str not in EMOJI_TO_LANGUAGE:
        logger.info(f"Emoji {emoji_str} not in supported languages")
        return
    
    language_code = EMOJI_TO_LANGUAGE[emoji_str]
    message = reaction.message
    
    # Skip if message is empty or from a bot
    if not message.content or message.author.bot:
        return
    
    try:
        # Check if thread already exists for this message
        thread = None
        message_id = message.id
        
        if message_id in active_threads:
            thread = active_threads[message_id]['thread']
        
        # Create new thread if none exists
        if thread is None:
            try:
                thread = await message.create_thread(
                    name=f"Translations for message",
                    auto_archive_duration=60  # 1 hour auto-archive
                )
                logger.info(f"Created thread {thread.id} for message {message.id}")
                
                # Store thread info and schedule deletion
                active_threads[message_id] = {
                    'thread': thread,
                    'translations': set()
                }
                
                # Schedule thread deletion after 180 seconds
                task = asyncio.create_task(delete_thread_after_delay(thread, message_id))
                thread_deletion_tasks[message_id] = task
                
            except discord.Forbidden:
                logger.error(f"No permission to create thread for message {message.id}")
                return
            except discord.HTTPException as e:
                logger.error(f"Failed to create thread: {e}")
                return
        
        # Check if this language was already translated
        if language_code in active_threads[message_id]['translations']:
            logger.info(f"Language {language_code} already translated for message {message.id}")
            return
        
        # Cancel existing deletion task and schedule a new one (reset timer)
        if message_id in thread_deletion_tasks:
            thread_deletion_tasks[message_id].cancel()
            logger.info(f"Cancelled previous deletion task for thread {thread.id}")
        
        # Schedule new deletion task with reset timer
        task = asyncio.create_task(delete_thread_after_delay(thread, message_id))
        thread_deletion_tasks[message_id] = task
        logger.info(f"Reset 180s deletion timer for thread {thread.id}")
        
        # Translate the message
        logger.info(f"Translating message to {language_code}")
        translated_text = await translation_service.translate(message.content, language_code)
        
        # Mark this language as translated
        active_threads[message_id]['translations'].add(language_code)
        
        # Get language name for display
        language_name = get_language_name(language_code)
        
        # Post translation in thread
        embed = discord.Embed(
            title=f"Translation ({language_name})",
            description=translated_text,
            color=0x00ff00
        )
        embed.set_footer(text=f"Translated by {user.display_name}")
        
        await thread.send(embed=embed)
        logger.info(f"Posted translation to thread {thread.id}")
        
    except Exception as e:
        logger.error(f"Error handling reaction: {e}")
        if thread:
            try:
                await thread.send(f"❌ Translation error: {str(e)}")
            except:
                pass

async def delete_thread_after_delay(thread, message_id):
    """Delete thread after 180 seconds delay"""
    try:
        logger.info(f"Scheduled thread {thread.id} for deletion in 180 seconds")
        await asyncio.sleep(180)  # Wait 3 minutes
        
        # Check if thread still exists in active_threads
        if message_id in active_threads:
            try:
                await thread.delete()
                logger.info(f"Successfully deleted thread {thread.id} after 180 seconds")
            except discord.NotFound:
                logger.info(f"Thread {thread.id} already deleted")
            except discord.Forbidden:
                logger.error(f"No permission to delete thread {thread.id}")
            except Exception as e:
                logger.error(f"Error deleting thread {thread.id}: {e}")
            finally:
                # Remove from active threads and tasks
                if message_id in active_threads:
                    del active_threads[message_id]
                    logger.info(f"Removed message {message_id} from active_threads")
                if message_id in thread_deletion_tasks:
                    del thread_deletion_tasks[message_id]
                    logger.info(f"Removed deletion task for message {message_id}")
    
    except asyncio.CancelledError:
        logger.info(f"Thread deletion task cancelled for thread {thread.id} (timer reset)")
        # Don't clean up here since the task was cancelled for timer reset
        raise  # Re-raise to properly handle cancellation
    except Exception as e:
        logger.error(f"Error in delete_thread_after_delay: {e}")

def get_language_name(language_code):
    """Get human-readable language name from code"""
    language_names = {
        'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
        'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
        'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
        'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh': 'Chinese', 'co': 'Corsican',
        'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch',
        'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino',
        'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician',
        'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati',
        'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew',
        'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic',
        'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian',
        'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh',
        'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish', 'ky': 'Kyrgyz',
        'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian',
        'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay',
        'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi',
        'mn': 'Mongolian', 'my': 'Myanmar', 'ne': 'Nepali', 'no': 'Norwegian',
        'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese',
        'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan',
        'gd': 'Scottish Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona',
        'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
        'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili',
        'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu',
        'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
        'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa',
        'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
    }
    return language_names.get(language_code, language_code.upper())

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle bot errors"""
    logger.error(f"Error in {event}: {args}, {kwargs}")

if __name__ == "__main__":
    try:
        bot.run(BOT_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        # Auto-restart on crashes for production
        import time
        time.sleep(5)
        logger.info("Attempting to restart bot...")
        try:
            bot.run(BOT_TOKEN)
        except Exception as restart_error:
            logger.error(f"Restart failed: {restart_error}")
