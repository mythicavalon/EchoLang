#!/usr/bin/env python3
"""
Discord Bot Invite Link Generator
Generates an invite link for the EchoLang translation bot
"""

import os

def generate_invite_link():
    """Generate Discord bot invite link with required permissions"""
    
    # Bot permissions needed for translation functionality
    permissions = [
        'read_messages',           # Read message history
        'send_messages',           # Send messages in threads
        'create_public_threads',   # Create threads for translations
        'send_messages_in_threads', # Send messages in threads
        'manage_threads',          # Manage thread lifecycle
        'read_message_history',    # Read message content for translation
        'add_reactions',           # Add reactions (optional)
        'use_external_emojis',     # Use flag emojis from other servers
    ]
    
    # Calculate permission integer (bitwise)
    # These are the Discord permission bit values
    permission_bits = {
        'read_messages': 1024,
        'send_messages': 2048,
        'create_public_threads': 34359738368,
        'send_messages_in_threads': 274877906944,
        'manage_threads': 17179869184,
        'read_message_history': 65536,
        'add_reactions': 64,
        'use_external_emojis': 262144,
    }
    
    total_permissions = sum(permission_bits.get(perm, 0) for perm in permissions)
    
    # Bot application ID (you'll need to get this from Discord Developer Portal)
    print("To generate the invite link, you need your bot's Application ID:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Select your bot application")
    print("3. Copy the 'Application ID' from the General Information page")
    print()
    
    app_id = input("Enter your bot's Application ID: ").strip()
    
    if not app_id:
        print("No Application ID provided. Using placeholder...")
        app_id = "YOUR_BOT_APPLICATION_ID"
    
    # Generate the invite URL
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions={total_permissions}&scope=bot"
    
    print(f"\n🔗 Bot Invite Link:")
    print(f"{invite_url}")
    print()
    print("📋 Required Permissions:")
    for perm in permissions:
        print(f"  • {perm.replace('_', ' ').title()}")
    print()
    print("🎯 How to use:")
    print("1. Copy the invite link above")
    print("2. Paste it in your browser")
    print("3. Select the Discord server where you want to add the bot")
    print("4. Authorize the bot with the required permissions")
    print("5. Test the bot by reacting to a message with a flag emoji (like 🇫🇷 or 🇯🇵)")
    
    return invite_url

if __name__ == "__main__":
    generate_invite_link()