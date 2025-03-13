"""
Study Sphere AI - Error Handler Module
This module handles error handling and message splitting for the Study Sphere AI bot
"""

import traceback
import time

class ErrorHandler:
    """
    Class to handle errors and message splitting for the Study Sphere AI bot
    """
    
    def __init__(self, telegram_api):
        """
        Initialize the ErrorHandler with the Telegram API
        
        Args:
            telegram_api: Instance of TelegramAPI class
        """
        self.telegram_api = telegram_api
        self.max_message_length = 4096  # Telegram's maximum message length
    
    def handle_error(self, chat_id, error, error_type="General Error"):
        """
        Handle errors by sending appropriate error messages to the user
        
        Args:
            chat_id (int): Chat ID to send error message to
            error (Exception): The error that occurred
            error_type (str): Type of error for better context
            
        Returns:
            bool: True if error was handled, False otherwise
        """
        try:
            # Log the error
            print(f"❌ {error_type}: {error}")
            print(traceback.format_exc())
            
            # Send error message to user
            error_message = f"❌ <b>Oops! Something went wrong</b>\n\n"
            
            if error_type == "API Error":
                error_message += (
                    "I couldn't connect to the knowledge database at the moment. "
                    "This might be due to high traffic or temporary issues.\n\n"
                    "Please try again in a few moments or choose a different option."
                )
            elif error_type == "Content Generation Error":
                error_message += (
                    "I had trouble generating the content you requested. "
                    "This might be due to the complexity of the topic or temporary issues.\n\n"
                    "Please try again with a different chapter or resource type."
                )
            else:
                error_message += (
                    "I encountered an unexpected issue while processing your request.\n\n"
                    "Please try again or start over with a new selection."
                )
            
            # Add retry button
            retry_keyboard = {
                "inline_keyboard": [
                    [{"text": "🔄 Try Again", "callback_data": "retry"}],
                    [{"text": "🏠 Start Over", "callback_data": "post:start_over"}]
                ]
            }
            
            self.telegram_api.send_message(chat_id, error_message, retry_keyboard)
            return True
            
        except Exception as e:
            # If error handling itself fails, log it but don't try to send more messages
            print(f"❌ Error in error handler: {e}")
            return False
    
    def split_and_send_message(self, chat_id, text, reply_markup=None):
        """
        Split long messages and send them in chunks
        
        Args:
            chat_id (int): Chat ID to send message to
            text (str): Message text to send
            reply_markup (dict, optional): Inline keyboard markup
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            # If message is within limits, send it directly
            if len(text) <= self.max_message_length:
                return self.telegram_api.send_message(chat_id, text, reply_markup)
            
            # Split message into chunks
            chunks = self._split_text(text)
            
            # Send each chunk
            for i, chunk in enumerate(chunks):
                # Add part indicator for multi-part messages
                if len(chunks) > 1:
                    part_indicator = f"<i>Part {i+1}/{len(chunks)}</i>\n\n"
                    chunk = part_indicator + chunk
                
                # Only add reply markup to the last chunk
                chunk_reply_markup = reply_markup if i == len(chunks) - 1 else None
                
                # Send chunk
                result = self.telegram_api.send_message(chat_id, chunk, chunk_reply_markup)
                
                # If sending fails, return the error
                if not result.get("ok", False):
                    return result
                
                # Small delay between messages to avoid rate limiting
                if i < len(chunks) - 1:
                    time.sleep(0.5)
            
            return {"ok": True, "result": "Message sent in multiple parts"}
            
        except Exception as e:
            print(f"❌ Error splitting and sending message: {e}")
            return {"ok": False, "error": str(e)}
    
    def _split_text(self, text, max_length=4000):
        """
        Split text into chunks of maximum length
        
        Args:
            text (str): Text to split
            max_length (int): Maximum length of each chunk
            
        Returns:
            list: List of text chunks
        """
        # Use a slightly smaller max_length to account for part indicators
        max_length = max_length - 50
        
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        lines = text.split('\n')
        current_chunk = ""
        
        for line in lines:
            # If adding this line would exceed max_length, start a new chunk
            if len(current_chunk) + len(line) + 1 > max_length:
                # If the current line itself is too long, split it
                if len(line) > max_length:
                    # If current_chunk is not empty, add it to chunks
                    if current_chunk:
                        chunks.append(current_chunk)
                    
                    # Split the long line into multiple chunks
                    for i in range(0, len(line), max_length):
                        sub_line = line[i:i + max_length]
                        chunks.append(sub_line)
                    
                    current_chunk = ""
                else:
                    # Add current chunk to chunks and start a new one with this line
                    chunks.append(current_chunk)
                    current_chunk = line
            else:
                # Add line to current chunk
                if current_chunk:
                    current_chunk += '\n' + line
                else:
                    current_chunk = line
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def handle_api_response(self, chat_id, response, reply_markup=None):
        """
        Handle API response and send appropriate message to user
        
        Args:
            chat_id (int): Chat ID to send message to
            response (str): API response
            reply_markup (dict, optional): Inline keyboard markup
            
        Returns:
            bool: True if response was handled successfully, False otherwise
        """
        try:
            # Check if response is an error message
            if response.startswith("❌ Error:"):
                error_message = f"❌ <b>API Error</b>\n\n{response[8:]}\n\nPlease try again or choose a different option."
                self.telegram_api.send_message(chat_id, error_message, reply_markup)
                return False
            
            # Split and send the response
            return self.split_and_send_message(chat_id, response, reply_markup)
            
        except Exception as e:
            return self.handle_error(chat_id, e, "Response Handling Error")
