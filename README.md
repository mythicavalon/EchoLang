# 🌍 EchoLang — Real-Time Discord Translation Bot

**EchoLang** is a powerful Discord bot that automatically translates messages using flag emoji reactions. Built for global communities to communicate seamlessly across language barriers.

## ✨ Features

- 🏴 **Flag Emoji Translation**  
  React to any message with a country flag emoji (🇪🇸🇫🇷🇩🇪🇯🇵🇰🇷🇨🇳) — EchoLang instantly translates the message into that language.

- 🧵 **Smart Thread Management**  
  Translations appear in auto-created threads attached to the original message, keeping conversations organized and clutter-free.

- ⏰ **Auto-Cleanup**  
  Translation threads automatically delete after 180 seconds, ensuring your server stays clean.

- 🌍 **100+ Languages Supported**  
  Powered by Google Translate via `deep-translator`, supporting virtually every major language with automatic source detection.

- 🛡️ **Robust Error Handling**  
  Graceful fallbacks, retry logic, and user-friendly error messages ensure reliable operation.

- ⚡ **Production Ready**  
  Built with Python 3.13, discord.py, and modern async patterns. Deployed on cloud platforms for 24/7 uptime.

## 🚀 Quick Start

### Using the Bot
1. Invite EchoLang to your Discord server
2. Write any message in a channel
3. React with a flag emoji (e.g., 🇪🇸 for Spanish, 🇫🇷 for French)
4. Watch the translation appear in a thread!

### Commands
- `!help` - Show bot information and usage guide
- `!info` - Display bot features and developer info
- `!about` - Bot credits and support information

## 🛠️ Technical Details

### Built With
- **Python 3.13+** - Modern async/await patterns
- **discord.py 2.5+** - Discord API integration
- **deep-translator** - Google Translate interface
- **Railway** - Cloud hosting platform

### Architecture
- **ThreadManager** - Handles thread lifecycle and guaranteed cleanup
- **TranslationHandler** - Manages translation requests with retry logic
- **Error Handling** - Comprehensive error management with user feedback

## 📦 Deployment

### Requirements
```
discord.py>=2.5.2
deep-translator>=1.11.4
```

### Environment Variables
```
DISCORD_BOT_TOKEN=your_bot_token_here
```

### Supported Platforms
- Railway (recommended)
- Render
- Fly.io
- Heroku
- Any Python 3.11+ hosting platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

Open source project - feel free to use and modify!

## 👨‍💻 Developer

**Created by [mythicavalon](https://github.com/mythicavalon)**

- Discord: Contact via server where bot is deployed
- GitHub: [@mythicavalon](https://github.com/mythicavalon)

---

**EchoLang** • *Breaking language barriers, one emoji at a time* 🌍
