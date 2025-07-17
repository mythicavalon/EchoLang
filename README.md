# EchoLang Discord Translation Bot

A Discord bot that translates messages in real-time using emoji reactions and Google Translate API.

## 🚀 Getting Your Bot Invite Link

To invite the EchoLang bot to your Discord server:

### Step 1: Get Your Application ID
1. Go to https://discord.com/developers/applications
2. Select your bot application (the one you created for EchoLang)
3. Copy the **Application ID** from the General Information page

### Step 2: Create Invite Link
Replace `YOUR_BOT_APPLICATION_ID` with your actual Application ID in this URL:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_APPLICATION_ID&permissions=377891938368&scope=bot
```

**Example:**
If your Application ID is `123456789012345678`, your invite link would be:
```
https://discord.com/api/oauth2/authorize?client_id=123456789012345678&permissions=377891938368&scope=bot
```

### Step 3: Required Permissions
The bot needs these permissions to work properly:
- **Read Messages** - To read message content for translation
- **Send Messages** - To send translations in threads
- **Create Public Threads** - To create translation threads
- **Send Messages in Threads** - To post translations
- **Manage Threads** - To clean up threads after 3 minutes
- **Read Message History** - To access message content
- **Add Reactions** - To react to messages (optional)
- **Use External Emojis** - To use flag emojis from other servers

## 🎯 How to Use

1. **Add the bot to your server** using the invite link above
2. **React to any message** with a flag emoji (like 🇫🇷 for French, 🇯🇵 for Japanese)
3. **The bot will create a thread** and post the translation there
4. **Multiple languages** can be translated in the same thread
5. **Threads auto-delete** after 3 minutes to keep channels clean

## 🌍 Supported Languages

The bot supports 150+ languages through country flag emojis:
- 🇺🇸 🇬🇧 → English
- 🇫🇷 → French  
- 🇩🇪 → German
- 🇪🇸 → Spanish
- 🇮🇹 → Italian
- 🇯🇵 → Japanese
- 🇰🇷 → Korean
- 🇨🇳 → Chinese
- 🇷🇺 → Russian
- 🇵🇹 🇧🇷 → Portuguese
- And many more...

## 🛠️ Technical Details

- **Framework:** Discord.py
- **Translation:** Google Translate API (googletrans==4.0.0-rc1)
- **Architecture:** Event-driven with automatic thread management
- **Rate Limiting:** Built-in 0.5s delay between requests
- **Auto-cleanup:** Threads delete after 180 seconds

## 📋 Bot Status

The bot is currently running and ready to translate messages. Make sure to:
1. Enable "Message Content Intent" in your bot settings
2. Give the bot the required permissions listed above
3. Test with a simple message and flag emoji reaction

## 🔧 Troubleshooting

- **Bot not responding:** Check if it has the required permissions
- **No thread created:** Ensure the bot can create threads in the channel
- **Translation failed:** The bot will show "[Translation error]" if Google Translate is unavailable
- **Bot offline:** Restart the bot using the workflow controls

---

**Ready to translate!** React with any flag emoji to start translating messages instantly.