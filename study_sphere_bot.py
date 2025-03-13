#!/usr/bin/env python3
"""
Study Sphere AI - Telegram Study Assistant Bot
A comprehensive bot designed to help students study by generating important questions,
summaries, notes, and other educational resources for all subjects and chapters.

Author: Study Sphere AI Team
Version: 1.0.0
Date: March 2025
"""

import json
import urllib.request
import urllib.parse
import time
import ssl
import re
import traceback
import sys

# Import custom modules
from telegram_api import TelegramAPI
from deepseek_api import DeepSeekAPI
from menu_navigation import MenuNavigation
from content_generator import ContentGenerator
from error_handler import ErrorHandler
from user_experience import UserExperience
from navigation_handler import NavigationHandler
from course_data import COURSE_DATA, RESOURCE_TYPES, DIFFICULTY_LEVELS

# ========================
# Configuration Constants
# ========================
TELEGRAM_BOT_TOKEN = "7762013839:AAEggfGexgFFwC5TEu7HDZoQcOO9x01Qab8"
DEEP_SEEK_API_KEY = "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"
DEEP_SEEK_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEP_SEEK_MODEL = "deepseek/deepseek-r1-zero:free"

class StudySphereBot:
    """
    Main bot class that orchestrates all components and handles the main loop
    """
    
    def __init__(self):
        """
        Initialize the Study Sphere AI bot with all required components
        """
        print("🚀 Initializing Study Sphere AI Bot...")
        
        # Initialize API clients
        self.telegram_api = TelegramAPI(TELEGRAM_BOT_TOKEN)
        self.deepseek_api = DeepSeekAPI(DEEP_SEEK_API_KEY, DEEP_SEEK_BASE_URL, DEEP_SEEK_MODEL)
        
        # Initialize helper modules
        self.menu_navigation = MenuNavigation()
        self.content_generator = ContentGenerator(DEEP_SEEK_API_KEY, DEEP_SEEK_BASE_URL, DEEP_SEEK_MODEL)
        self.user_experience = UserExperience()
        self.error_handler = ErrorHandler(self.telegram_api)
        self.navigation_handler = NavigationHandler(self.menu_navigation, self.user_experience)
        
        print("✅ Bot components initialized successfully")
    
    def start(self):
        """
        Start the bot and begin processing updates
        """
        print("🔄 Starting Study Sphere AI Bot...")
        
        # Delete any existing webhook
        self.telegram_api.delete_webhook()
        print("✅ Webhook deleted")
        
        print("🔄 Bot is now running. Press Ctrl+C to stop.")
        
        # Main loop
        while True:
            try:
                # Get updates from Telegram API
                updates = self.telegram_api.process_updates()
                
                # Process each update
                for update in updates:
                    self._process_update(update)
                    
                # Small delay to avoid excessive API calls
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("👋 Bot stopped by user")
                break
                
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                print(traceback.format_exc())
                time.sleep(5)  # Wait before retrying
    
    def _process_update(self, update):
        """
        Process a single update from Telegram API
        
        Args:
            update (dict): Update from Telegram API
        """
        try:
            # Handle message
            if "message" in update:
                self._handle_message(update["message"])
                
            # Handle callback query
            if "callback_query" in update:
                self._handle_callback_query(update["callback_query"])
                
        except Exception as e:
            print(f"❌ Error processing update: {e}")
            print(traceback.format_exc())
            
            # Try to send error message to user if possible
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                self.error_handler.handle_error(chat_id, e)
            elif "callback_query" in update:
                chat_id = update["callback_query"]["message"]["chat"]["id"]
                self.error_handler.handle_error(chat_id, e)
    
    def _handle_message(self, message):
        """
        Handle a message from a user
        
        Args:
            message (dict): Message from Telegram API
        """
        # Extract message data
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        # Handle /start command
        if text == "/start":
            self.navigation_handler.handle_start(chat_id, self.telegram_api)
            
        # Handle /help command
        elif text == "/help":
            help_message = (
                f"{self.user_experience.emojis['help']} <b>Study Sphere AI Help</b> {self.user_experience.emojis['book']}\n\n"
                f"I'm your personal study assistant designed to help you excel in your academics.\n\n"
                f"<b>Available Commands:</b>\n"
                f"• /start - Start or restart the bot\n"
                f"• /help - Show this help message\n\n"
                f"<b>How to use:</b>\n"
                f"1. Select your class (9-12)\n"
                f"2. Choose a subject\n"
                f"3. Select a chapter\n"
                f"4. Pick the type of study material you need\n"
                f"5. For questions, select a difficulty level\n\n"
                f"At any point, you can use the '🔙 Go Back' button to return to the previous menu."
            )
            self.telegram_api.send_message(chat_id, help_message)
            
        # Handle other messages
        else:
            # For now, just prompt the user to use /start
            message = (
                f"{self.user_experience.emojis['info']} Please use /start to begin using Study Sphere AI, "
                f"or /help to see available commands."
            )
            self.telegram_api.send_message(chat_id, message)
    
    def _handle_callback_query(self, callback_query):
        """
        Handle a callback query from an inline keyboard
        
        Args:
            callback_query (dict): Callback query from Telegram API
        """
        # Extract callback data
        callback_id = callback_query["id"]
        callback_data = callback_query.get("data", "")
        chat_id = callback_query["message"]["chat"]["id"]
        
        # Answer callback query to remove loading indicator
        self.telegram_api.answer_callback_query(callback_id)
        
        # Handle callback data
        self.navigation_handler.handle_callback(
            chat_id,
            callback_data,
            self.telegram_api,
            self.content_generator,
            self.error_handler
        )

def main():
    """
    Main entry point for the bot
    """
    print("📚 Study Sphere AI - Telegram Study Assistant Bot")
    print("================================================")
    
    # Create and start the bot
    bot = StudySphereBot()
    bot.start()

if __name__ == "__main__":
    main()
