# Discord Translation Bot

## Overview

This is a Discord bot that provides real-time message translation functionality through flag emoji reactions. Users can react to messages with flag emojis to translate the content into their desired language. The bot creates temporary threads for translations to keep channels organized and automatically manages thread lifecycle.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Architecture
- **Bot Framework**: Discord.py library for Discord API integration
- **Translation Service**: Google Translate API via googletrans library
- **Event-Driven Design**: Reaction-based triggers for translation requests
- **Thread Management**: Automatic thread creation and cleanup for organized translations

### Key Design Decisions
- **Reaction-Based Interface**: Users interact by adding flag emoji reactions to messages, providing an intuitive and non-intrusive translation experience
- **Thread Organization**: Translations are posted in temporary threads to avoid cluttering main channels
- **Rate Limiting**: Built-in delays between translation requests to prevent API abuse
- **Asynchronous Processing**: Non-blocking translation operations to maintain bot responsiveness

## Key Components

### 1. Main Bot Handler (`main.py`)
- Discord bot initialization with required intents
- Event handling for reactions and bot readiness
- Thread management and cleanup logic
- Integration with translation service

### 2. Translation Service (`translate.py`)
- Wrapper around Google Translate API
- Rate limiting implementation
- Async/await pattern for non-blocking operations
- Error handling and fallback responses

### 3. Language Configuration (`languages.py`)
- Mapping of flag emojis to language codes
- Supports 50+ languages through country flag emojis
- Handles multiple countries mapping to same language (e.g., 🇺🇸 and 🇬🇧 both map to English)

### 4. Configuration Management (`config.py`)
- Centralized configuration for bot settings
- Feature flags for optional functionality
- Logging configuration
- Rate limiting and thread management parameters

## Data Flow

1. **User Interaction**: User reacts to a message with a flag emoji
2. **Event Processing**: Bot receives `on_reaction_add` event
3. **Validation**: Bot validates emoji is a supported flag and message is translatable
4. **Translation Request**: Translation service processes the message content
5. **Thread Creation**: Bot creates a temporary thread for the translation
6. **Response Delivery**: Translated content is posted in the thread
7. **Cleanup**: Thread is automatically archived/deleted after timeout

## External Dependencies

### Required Libraries
- `discord.py`: Discord API integration
- `googletrans`: Google Translate API client
- `asyncio`: Asynchronous programming support
- `logging`: Application logging

### Environment Variables
- `DISCORD_BOT_TOKEN`: Discord bot authentication token

### External Services
- **Discord API**: For bot functionality and message handling
- **Google Translate API**: For translation services (accessed via googletrans library)

## Deployment Strategy

### Environment Setup
- Python 3.7+ runtime environment
- Discord bot token configuration
- Required Python packages installation

### Configuration
- Bot token must be set via environment variable
- Logging is configured for INFO level by default
- Rate limiting and thread management settings are configurable

### Scalability Considerations
- Built-in rate limiting prevents API abuse
- Thread-based organization reduces channel clutter
- Asynchronous design supports concurrent translation requests
- Memory management through automatic thread cleanup

### Feature Flags
- Language detection toggle
- Source language display option
- Auto-thread deletion control
- Rate limiting enable/disable
- Text length limiting

The architecture prioritizes user experience through intuitive emoji-based interactions while maintaining clean channel organization and responsible API usage.