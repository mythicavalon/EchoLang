# EchoLang Discord Translation Bot

A Discord bot that provides real-time message translation through flag emoji reactions. Users can react to messages with flag emojis to translate the content into their desired language.

## Features

- **Flag Emoji Reactions**: React with country flag emojis to translate messages
- **Thread Organization**: Creates temporary threads for translations to keep channels clean
- **Multi-language Support**: Supports 150+ languages via Google Translate API
- **Auto-cleanup**: Threads auto-delete after 180 seconds of inactivity
- **Timer Reset**: Thread deletion timer resets with each new translation request
- **Rate Limiting**: Built-in protection against API abuse

## Setup Instructions

### Prerequisites

- Python 3.7+
- Discord Bot Token
- Discord Server with appropriate permissions

### Installation

1. **Clone or Download** this repository
2. **Install dependencies**:
   ```bash
   pip install discord.py googletrans==4.0.0-rc1
   ```

3. **Configure the bot**:
   - Get your Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
   - Set the environment variable:
     ```bash
     export DISCORD_BOT_TOKEN="your_bot_token_here"
     ```

4. **Invite the bot** to your server:
   ```bash
   python bot_invite.py
   ```
   Follow the generated link to invite the bot with required permissions.

5. **Run the bot**:
   ```bash
   python main.py
   ```

### Required Bot Permissions

- Read Messages
- Send Messages
- Create Public Threads
- Send Messages in Threads
- Manage Threads
- Add Reactions
- Use External Emojis

## Usage

1. **React to any message** with a flag emoji (e.g., 🇯🇵 for Japanese, 🇪🇸 for Spanish)
2. **Bot creates a thread** under the message with the translation
3. **Multiple translations** can be added to the same thread
4. **Thread auto-deletes** after 180 seconds of no new reactions

## Supported Languages

The bot supports 150+ languages through country flag emojis:

- 🇺🇸 🇬🇧 → English
- 🇪🇸 🇲🇽 → Spanish  
- 🇯🇵 → Japanese
- 🇨🇳 → Chinese
- 🇫🇷 → French
- 🇩🇪 → German
- 🇮🇹 → Italian
- 🇷🇺 → Russian
- 🇰🇷 → Korean
- 🇮🇳 → Hindi
- And many more...

## File Structure

```
echolang-discord-bot/
├── main.py           # Main bot logic and event handling
├── translate.py      # Translation service wrapper
├── languages.py      # Flag emoji to language code mapping
├── config.py         # Configuration management
├── bot_invite.py     # Bot invitation helper
├── README.md         # This file
├── replit.md         # Technical architecture documentation
├── pyproject.toml    # Python dependencies
├── .gitignore        # Git ignore rules
└── uv.lock          # Dependencies lock file
```

## Technical Details

### Architecture

- **Event-driven**: Uses Discord.py reaction events
- **Asynchronous**: Non-blocking translation operations
- **Thread-based**: Organized translation display
- **Rate-limited**: Prevents API abuse
- **Modular**: Clean separation of concerns

### Dependencies

- `discord.py` - Discord API integration
- `googletrans` - Google Translate API wrapper
- `asyncio` - Asynchronous programming support

### Configuration

Bot behavior can be customized in `config.py`:
- Thread auto-deletion timeout
- Rate limiting settings
- Logging configuration
- Feature toggles

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to reactions**:
   - Check bot permissions in the server
   - Verify the bot token is correct
   - Ensure the bot is online

2. **Translation errors**:
   - Google Translate API might be temporarily unavailable
   - Check internet connection
   - Verify the flag emoji is supported

3. **Thread creation fails**:
   - Bot needs "Create Public Threads" permission
   - Check channel permissions
   - Verify bot role hierarchy

### Support

For technical issues or feature requests, check the logs in your console for detailed error messages.

## License

This project is open source and available under the MIT License.