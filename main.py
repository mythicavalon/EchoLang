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

@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_reaction_add(reaction, user):
    """Handle emoji reactions added to messages"""
    # Ignore bot's own reactions
    if user.bot:
        return
    
    # Check if reaction is a flag emoji
    emoji_str = str(reaction.emoji)
    if emoji_str not in EMOJI_TO_LANGUAGE:
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
            # Check if thread still exists
            try:
                # Use the bot to fetch the thread instead of thread.fetch()
                await bot.fetch_channel(thread.id)
            except discord.NotFound:
                # Thread was deleted, remove from active threads
                del active_threads[message_id]
                thread = None
        
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
                asyncio.create_task(delete_thread_after_delay(thread, message_id))
                
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
        await asyncio.sleep(180)  # Wait 3 minutes
        
        # Check if thread still exists in active_threads
        if message_id in active_threads:
            try:
                await thread.delete()
                logger.info(f"Deleted thread {thread.id} after 180 seconds")
            except discord.NotFound:
                logger.info(f"Thread {thread.id} already deleted")
            except discord.Forbidden:
                logger.error(f"No permission to delete thread {thread.id}")
            except Exception as e:
                logger.error(f"Error deleting thread {thread.id}: {e}")
            finally:
                # Remove from active threads
                if message_id in active_threads:
                    del active_threads[message_id]
    
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
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
