import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'your_bot_token_here')

# Translation service configuration
TRANSLATION_CONFIG = {
    'rate_limit_delay': 0.5,  # Delay between translation requests in seconds
    'max_text_length': 1000,  # Maximum text length for translation
    'thread_auto_delete_delay': 180,  # Thread auto-delete delay in seconds (3 minutes)
    'thread_auto_archive_duration': 60,  # Thread auto-archive duration in minutes
}

# Discord configuration
DISCORD_CONFIG = {
    'command_prefix': '!',
    'thread_name_template': 'Translations for message',
    'embed_color': 0x00ff00,  # Green color for translation embeds
    'error_color': 0xff0000,  # Red color for error embeds
}

# Logging configuration
LOGGING_CONFIG = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_translation_requests': True,
    'log_thread_operations': True,
    'log_errors': True,
}

# Feature flags
FEATURE_FLAGS = {
    'enable_language_detection': True,
    'enable_source_language_display': True,
    'enable_auto_thread_deletion': True,
    'enable_rate_limiting': True,
    'enable_text_length_limiting': True,
}

# Error messages
ERROR_MESSAGES = {
    'translation_failed': '[Translation error]',
    'empty_message': '[Empty message]',
    'rate_limit_exceeded': '[Rate limit exceeded]',
    'text_too_long': '[Text too long]',
    'unsupported_language': '[Unsupported language]',
    'thread_creation_failed': '[Thread creation failed]',
    'permission_denied': '[Permission denied]',
    'unknown_error': '[Unknown error]',
}

# Validation
def validate_config():
    """Validate configuration settings"""
    issues = []
    
    if not BOT_TOKEN or BOT_TOKEN == 'your_bot_token_here':
        issues.append("BOT_TOKEN not set or using placeholder value")
    
    if TRANSLATION_CONFIG['rate_limit_delay'] < 0:
        issues.append("Rate limit delay cannot be negative")
    
    if TRANSLATION_CONFIG['max_text_length'] <= 0:
        issues.append("Max text length must be positive")
    
    if TRANSLATION_CONFIG['thread_auto_delete_delay'] <= 0:
        issues.append("Thread auto-delete delay must be positive")
    
    if issues:
        logger.warning("Configuration issues found:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    
    return len(issues) == 0

# Auto-validate on import
if __name__ == "__main__":
    validate_config()
