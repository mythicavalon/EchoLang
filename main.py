import discord
from discord.ext import commands
import asyncio
import logging
from translate import TranslationService
from languages import EMOJI_TO_LANGUAGE
from config import BOT_TOKEN
import threading
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

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

# Store active threads for cleanup - now with better structure
active_threads = {}
# Store thread deletion tasks for cancellation
thread_deletion_tasks = {}

class ThreadManager:
    """Manages thread lifecycle including guaranteed cleanup"""
    
    @staticmethod
    async def create_translation_thread(message, user):
        """Create a new translation thread with guaranteed cleanup scheduling"""
        try:
            thread = await message.create_thread(
                name=f"Translations for message",
                auto_archive_duration=60  # 1 hour auto-archive
            )
            logger.info(f"Created thread {thread.id} for message {message.id}")
            
            # Store thread info
            message_id = message.id
            active_threads[message_id] = {
                'thread': thread,
                'translations': set(),
                'created_at': time.time(),
                'creator': user.name
            }
            
            # ALWAYS schedule deletion - this is critical
            ThreadManager.schedule_thread_deletion(thread, message_id)
            
            return thread
            
        except discord.Forbidden:
            logger.error(f"No permission to create thread for message {message.id}")
            raise
        except discord.HTTPException as e:
            logger.error(f"Failed to create thread: {e}")
            raise
    
    @staticmethod
    def schedule_thread_deletion(thread, message_id):
        """Schedule thread deletion with guaranteed execution"""
        # Cancel any existing deletion task
        if message_id in thread_deletion_tasks:
            thread_deletion_tasks[message_id].cancel()
            logger.info(f"Cancelled previous deletion task for thread {thread.id}")
        
        # Schedule new deletion task
        task = asyncio.create_task(ThreadManager._delete_thread_after_delay(thread, message_id))
        thread_deletion_tasks[message_id] = task
        logger.info(f"Scheduled thread {thread.id} for deletion in 120 seconds")
    
    @staticmethod
    async def _delete_thread_after_delay(thread, message_id):
        """Delete thread after delay - guaranteed execution"""
        try:
            logger.info(f"Thread {thread.id} deletion countdown started (120s)")
            await asyncio.sleep(120)  # Wait 2 minutes
            
            # Attempt to delete the thread
            await ThreadManager._cleanup_thread(thread, message_id, "scheduled deletion")
            
        except asyncio.CancelledError:
            logger.info(f"Thread deletion task cancelled for thread {thread.id} (timer reset)")
            # Re-raise to properly handle cancellation
            raise
        except Exception as e:
            logger.error(f"Error in thread deletion task: {e}")
            # Even if there's an error, try to clean up
            await ThreadManager._cleanup_thread(thread, message_id, "error cleanup")
    
    @staticmethod
    async def _cleanup_thread(thread, message_id, reason):
        """Cleanup thread and associated data"""
        try:
            # Try to delete the thread
            await thread.delete()
            logger.info(f"Successfully deleted thread {thread.id} ({reason})")
        except discord.NotFound:
            logger.info(f"Thread {thread.id} already deleted ({reason})")
        except discord.Forbidden:
            logger.error(f"No permission to delete thread {thread.id} ({reason})")
        except Exception as e:
            logger.error(f"Error deleting thread {thread.id}: {e} ({reason})")
        finally:
            # ALWAYS clean up tracking data regardless of deletion success
            if message_id in active_threads:
                del active_threads[message_id]
                logger.info(f"Removed message {message_id} from active_threads ({reason})")
            if message_id in thread_deletion_tasks:
                del thread_deletion_tasks[message_id]
                logger.info(f"Removed deletion task for message {message_id} ({reason})")

class TranslationHandler:
    """Handles translation requests with proper error handling"""
    
    @staticmethod
    async def handle_translation_request(thread, message, language_code, user):
        """Handle a translation request with comprehensive error handling"""
        translation_posted = False
        error_message = None
        
        try:
            # Check if already translated
            message_id = message.id
            if message_id in active_threads and language_code in active_threads[message_id]['translations']:
                logger.info(f"Language {language_code} already translated for message {message.id}")
                return True
            
            # Reset the deletion timer since there's new activity
            ThreadManager.schedule_thread_deletion(thread, message_id)
            
            # Attempt translation
            logger.info(f"Translating message to {language_code}")
            translated_text = await translation_service.translate(message.content, language_code)
            
            # Check if translation was successful
            if translated_text and not translated_text.startswith('[') and not translated_text.startswith('Translation'):
                # Mark as translated
                active_threads[message_id]['translations'].add(language_code)
                
                # Create success embed
                language_name = get_language_name(language_code)
                embed = discord.Embed(
                    title=f"Translation ({language_name})",
                    description=translated_text,
                    color=0x00ff00
                )
                embed.set_footer(text=f"Translated by {user.display_name if hasattr(user, 'display_name') else user.name} • EchoLang by mythicavalon • Support: paypal.me/amalnair11")
                
                await thread.send(embed=embed)
                logger.info(f"Posted successful translation to thread {thread.id}")
                translation_posted = True
                
            else:
                # Translation failed - post error to thread
                error_message = translated_text if translated_text else "Translation service unavailable"
                
        except Exception as e:
            logger.error(f"Translation error: {e}")
            error_message = f"Translation error: {str(e)}"
        
        # If translation failed, post error message to thread
        if not translation_posted and error_message:
            try:
                language_name = get_language_name(language_code)
                error_embed = discord.Embed(
                    title=f"Translation Error ({language_name})",
                    description=f"❌ {error_message}",
                    color=0xff0000
                )
                error_embed.set_footer(text=f"Requested by {user.display_name if hasattr(user, 'display_name') else user.name}")
                
                await thread.send(embed=error_embed)
                logger.info(f"Posted error message to thread {thread.id}")
            except Exception as post_error:
                logger.error(f"Failed to post error message to thread: {post_error}")
        
        return translation_posted

@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    
    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="for flag reactions 🌍 | by mythicavalon"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    
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
        user = await get_user_from_payload(payload)
        if not user:
            logger.error(f"Could not resolve user {payload.user_id}")
            return
            
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

async def get_user_from_payload(payload):
    """Get user object from payload with multiple fallback methods"""
    user = None
    
    # Try to get channel for guild context
    channel = bot.get_channel(payload.channel_id)
    
    # Method 1: Guild member (works with members intent)
    if hasattr(channel, 'guild') and channel.guild:
        user = channel.guild.get_member(payload.user_id)
        if user:
            logger.info(f"Found user via guild member: {user.name}")
            return user
    
    # Method 2: Bot user cache
    user = bot.get_user(payload.user_id)
    if user:
        logger.info(f"Found user via bot cache: {user.name}")
        return user
    
    # Method 3: Fetch user directly
    try:
        user = await bot.fetch_user(payload.user_id)
        if user:
            logger.info(f"Found user via fetch: {user.name}")
            return user
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
    
    # Method 4: Create minimal user object as fallback
    class MinimalUser:
        def __init__(self, user_id):
            self.id = user_id
            self.name = f"User_{user_id}"
            self.bot = False
            
    user = MinimalUser(payload.user_id)
    logger.info(f"Using fallback user object for {payload.user_id}")
    return user

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
    
    thread = None
    try:
        # Check if thread already exists for this message
        message_id = message.id
        
        if message_id in active_threads:
            thread = active_threads[message_id]['thread']
            logger.info(f"Using existing thread {thread.id} for message {message.id}")
        else:
            # Create new thread
            thread = await ThreadManager.create_translation_thread(message, user)
        
        # Handle the translation request
        success = await TranslationHandler.handle_translation_request(
            thread, message, language_code, user
        )
        
        if success:
            logger.info(f"Successfully handled translation request for {language_code}")
        else:
            logger.warning(f"Translation request failed for {language_code}")
        
    except discord.Forbidden:
        logger.error(f"No permission to create thread for message {message.id}")
        # If we can't create a thread, try to react with an error emoji
        try:
            await message.add_reaction('❌')
        except:
            pass
    except Exception as e:
        logger.error(f"Error handling reaction: {e}")
        # If we have a thread, try to post the error there
        if thread:
            try:
                error_embed = discord.Embed(
                    title="System Error",
                    description=f"❌ An unexpected error occurred: {str(e)}",
                    color=0xff0000
                )
                await thread.send(embed=error_embed)
            except Exception as post_error:
                logger.error(f"Failed to post system error to thread: {post_error}")

@bot.command(name='info', aliases=['about', 'echolang'])
async def info_command(ctx):
    """Show bot information and usage instructions"""
    embed = discord.Embed(
        title="🌍 EchoLang Translation Bot",
        description="Automatic message translation using flag emoji reactions",
        color=0x00ff00
    )
    
    embed.add_field(
        name="📖 How to Use",
        value="React to any message with a flag emoji (🇪🇸🇫🇷🇩🇪🇯🇵🇰🇷🇨🇳 etc.) to get an instant translation!",
        inline=False
    )
    
    embed.add_field(
        name="✨ Features",
        value="• Auto-creates translation threads\n• Supports 100+ languages\n• Threads auto-delete after 2 minutes\n• Smart error handling",
        inline=False
    )
    
    embed.add_field(
        name="🛠️ Developer",
        value="**mythicavalon**\nBuilt with Python, discord.py & deep-translator",
        inline=True
    )
    
    embed.add_field(
        name="🔗 Commands",
        value="Use `!info`, `!about`, or `!echolang` for help",
        inline=True
    )
    
    embed.add_field(
        name="☕ Support Development",
        value="**[$20 - Server Hosting](https://paypal.me/amalnair11/20)** • **[$40 - Premium Features](https://paypal.me/amalnair11/40)** • **[Custom Amount](https://paypal.me/amalnair11)**\n*Help keep EchoLang running 24/7 and fund new features!*",
        inline=False
    )
    
    embed.set_footer(text="EchoLang • Made with ❤️ by mythicavalon")
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    
    await ctx.send(embed=embed)

@bot.command(name='donate', aliases=['support', 'funding'])
async def donate_command(ctx):
    """Show donation information and support tiers"""
    embed = discord.Embed(
        title="☕ Support EchoLang Development",
        description="Help keep EchoLang running and fund new features!",
        color=0xFFD700  # Gold color
    )
    
    embed.add_field(
        name="💰 Donation Tiers",
        value=(
            "**$20 - Server Hosting** 🌐\n"
            "├ 1 month hosting costs\n"
            "├ 24/7 reliable uptime\n"
            "└ Bug fixes & maintenance\n\n"
            "**$40 - Premium Features** ✨\n"
            "├ All $20 benefits included\n"
            "├ Priority feature development\n"
            "├ New language support\n"
            "└ Performance optimizations"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔗 Donation Links",
        value=(
            "**[$20 Hosting](https://paypal.me/amalnair11/20)** • "
            "**[$40 Features](https://paypal.me/amalnair11/40)** • "
            "**[Custom Amount](https://paypal.me/amalnair11)**"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎯 Why Support?",
        value="Your donations directly fund server costs, new features, and keep EchoLang free for everyone!",
        inline=False
    )
    
    embed.set_footer(text="Thank you for considering supporting EchoLang! ❤️")
    embed.set_thumbnail(url="https://ko-fi.com/img/githubbutton_sm.svg")
    
    await ctx.send(embed=embed)

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

# Health check server for Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"EchoLang Bot is running")
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass

def start_health_server():
    """Start health check server for Render"""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"Health server starting on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # Start health server in background
    threading.Thread(target=start_health_server, daemon=True).start()
    
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
