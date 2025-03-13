"""
Study Sphere AI - Telegram API Module
This module handles all Telegram API interactions for the Study Sphere AI bot
"""

import json
import urllib.request
import urllib.parse
import time
import ssl

class TelegramAPI:
    """
    Class to handle all Telegram API interactions
    """
    
    def __init__(self, token):
        """
        Initialize the TelegramAPI with the bot token
        
        Args:
            token (str): Telegram Bot API token
        """
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        self.update_offset = None
        
        # Create SSL context that ignores certificate verification
        # This is sometimes needed for API calls in certain environments
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
    
    def delete_webhook(self):
        """
        Delete any existing webhook to use getUpdates method
        
        Returns:
            dict: Response from Telegram API
        """
        url = self.api_url + "setWebhook"
        data = urllib.parse.urlencode({"url": ""}).encode()
        req = urllib.request.Request(url, data=data)
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                result = json.loads(response.read().decode())
                print(f"🔄 Webhook status: {result}")
                return result
        except Exception as e:
            print(f"❌ Error deleting webhook: {e}")
            return {"ok": False, "error": str(e)}
    
    def get_updates(self, timeout=30):
        """
        Get updates from Telegram API using long polling
        
        Args:
            timeout (int): Timeout for long polling in seconds
            
        Returns:
            dict: Updates from Telegram API
        """
        params = {
            "timeout": timeout
        }
        
        if self.update_offset:
            params["offset"] = self.update_offset
            
        url = self.api_url + "getUpdates?" + urllib.parse.urlencode(params)
        
        try:
            with urllib.request.urlopen(url, timeout=timeout+10, context=self.ssl_context) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"❌ Error getting updates: {e}")
            return {"ok": False, "error": str(e)}
    
    def send_message(self, chat_id, text, reply_markup=None, parse_mode="HTML"):
        """
        Send message to a chat
        
        Args:
            chat_id (int): Chat ID to send message to
            text (str): Message text
            reply_markup (dict, optional): Inline keyboard markup
            parse_mode (str, optional): Parse mode for message formatting
            
        Returns:
            dict: Response from Telegram API
        """
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
            
        encoded_data = urllib.parse.urlencode(data).encode()
        url = self.api_url + "sendMessage"
        req = urllib.request.Request(url, data=encoded_data)
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_message = e.read().decode()
            print(f"❌ HTTP Error sending message: {e.code} - {error_message}")
            
            # If message is too long, return special error
            if e.code == 400 and "message is too long" in error_message.lower():
                return {"ok": False, "error": "MESSAGE_TOO_LONG"}
                
            return {"ok": False, "error": error_message}
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return {"ok": False, "error": str(e)}
    
    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        """
        Answer a callback query
        
        Args:
            callback_query_id (str): Callback query ID
            text (str, optional): Text to show to user
            show_alert (bool, optional): Whether to show as alert
            
        Returns:
            dict: Response from Telegram API
        """
        data = {
            "callback_query_id": callback_query_id
        }
        
        if text:
            data["text"] = text
            
        data["show_alert"] = show_alert
        
        encoded_data = urllib.parse.urlencode(data).encode()
        url = self.api_url + "answerCallbackQuery"
        req = urllib.request.Request(url, data=encoded_data)
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"❌ Error answering callback query: {e}")
            return {"ok": False, "error": str(e)}
    
    def edit_message_text(self, chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
        """
        Edit a message's text
        
        Args:
            chat_id (int): Chat ID
            message_id (int): Message ID to edit
            text (str): New text
            reply_markup (dict, optional): New inline keyboard markup
            parse_mode (str, optional): Parse mode for message formatting
            
        Returns:
            dict: Response from Telegram API
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
            
        encoded_data = urllib.parse.urlencode(data).encode()
        url = self.api_url + "editMessageText"
        req = urllib.request.Request(url, data=encoded_data)
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"❌ Error editing message: {e}")
            return {"ok": False, "error": str(e)}
    
    def send_chat_action(self, chat_id, action="typing"):
        """
        Send chat action to indicate bot is performing an action
        
        Args:
            chat_id (int): Chat ID
            action (str, optional): Action type (typing, upload_photo, etc.)
            
        Returns:
            dict: Response from Telegram API
        """
        data = {
            "chat_id": chat_id,
            "action": action
        }
        
        encoded_data = urllib.parse.urlencode(data).encode()
        url = self.api_url + "sendChatAction"
        req = urllib.request.Request(url, data=encoded_data)
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"❌ Error sending chat action: {e}")
            return {"ok": False, "error": str(e)}
    
    def process_updates(self):
        """
        Process updates from Telegram API
        
        Returns:
            list: List of processed updates
        """
        updates_response = self.get_updates()
        
        if not updates_response.get("ok", False):
            print(f"❌ Failed to get updates: {updates_response.get('error', 'Unknown error')}")
            time.sleep(5)  # Wait before retrying
            return []
            
        updates = updates_response.get("result", [])
        
        if updates:
            # Update the offset to acknowledge processed updates
            self.update_offset = updates[-1]["update_id"] + 1
            
        return updates
