"""
Telegram message handler for trading signals

Reads trading signals and alerts from Telegram channels.
"""

from typing import Optional, Dict, Any, Callable
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class TelegramHandler:
    """Handler for reading Telegram channel messages."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Telegram handler.
        
        Args:
            config: Telegram configuration dictionary
                   {
                       'api_id': 'your_api_id',
                       'api_hash': 'your_api_hash',
                       'bot_token': 'your_bot_token',
                       'channel_id': 12345678,
                       'phone_number': '+1234567890'
                   }
        """
        self.config = config
        self.api_id = config.get('api_id')
        self.api_hash = config.get('api_hash')
        self.bot_token = config.get('bot_token')
        self.channel_id = config.get('channel_id')
        self.phone_number = config.get('phone_number')
        
        self.client = None
        self.message_handlers = []
        
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration."""
        if not self.api_id or not self.api_hash:
            logger.warning("Telegram API ID and Hash not configured")
        if not self.channel_id:
            logger.warning("Telegram channel ID not configured")
    
    async def connect(self) -> bool:
        """
        Connect to Telegram.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            from telethon import TelegramClient
            
            self.client = TelegramClient(
                'trading_bot_session',
                self.api_id,
                self.api_hash
            )
            
            await self.client.start(phone=self.phone_number)
            logger.info("Connected to Telegram")
            return True
            
        except ImportError:
            logger.error("telethon not installed. Install with: pip install telethon")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected from Telegram")
    
    def register_handler(self, handler: Callable) -> None:
        """
        Register a message handler function.
        
        Args:
            handler: Async function to handle messages
        """
        self.message_handlers.append(handler)
        logger.info(f"Registered message handler: {handler.__name__}")
    
    async def listen_for_messages(self) -> None:
        """Listen for new messages in configured channel."""
        if not self.client:
            logger.error("Not connected to Telegram")
            return
        
        try:
            from telethon import events
            
            @self.client.on(events.NewMessage(chats=self.channel_id))
            async def handle_new_message(event):
                message = event.message
                await self._process_message(message)
            
            logger.info(f"Listening for messages on channel {self.channel_id}")
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Error listening for messages: {e}")
    
    async def _process_message(self, message) -> None:
        """
        Process received message.
        
        Args:
            message: Telethon message object
        """
        try:
            message_data = {
                'id': message.id,
                'text': message.text,
                'timestamp': message.date,
                'sender_id': message.sender_id,
                'raw_message': message,
            }
            
            logger.info(f"Received message: {message_data['text'][:100]}")
            
            # Call all registered handlers
            for handler in self.message_handlers:
                try:
                    await handler(message_data)
                except Exception as e:
                    logger.error(f"Error in message handler: {e}")
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def get_channel_messages(
        self,
        limit: int = 100,
        offset_date=None
    ) -> list:
        """
        Get historical messages from channel.
        
        Args:
            limit: Number of messages to retrieve
            offset_date: Get messages before this date
            
        Returns:
            List of messages
        """
        if not self.client:
            logger.error("Not connected to Telegram")
            return []
        
        try:
            messages = await self.client.get_messages(
                self.channel_id,
                limit=limit,
                offset_date=offset_date
            )
            
            logger.info(f"Retrieved {len(messages)} messages from channel")
            return messages
        
        except Exception as e:
            logger.error(f"Error retrieving channel messages: {e}")
            return []
    
    async def send_message(self, text: str) -> Optional[int]:
        """
        Send a message to the configured channel.
        
        Args:
            text: Message text
            
        Returns:
            Message ID if successful, None otherwise
        """
        if not self.client:
            logger.error("Not connected to Telegram")
            return None
        
        try:
            message = await self.client.send_message(self.channel_id, text)
            logger.info(f"Sent message to channel: {text[:50]}")
            return message.id
        
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None


class TelegramSignalParser:
    """Parse trading signals from Telegram messages."""
    
    @staticmethod
    def parse_signal(text: str) -> Optional[Dict[str, Any]]:
        """
        Parse trading signal from message text.
        
        Expected format examples:
        - "BUY AAPL at 150.50"
        - "SELL BTC/USD at 45000"
        - "HOLD SPY"
        
        Args:
            text: Message text
            
        Returns:
            Dictionary with parsed signal or None
        """
        if not text:
            return None
        
        text_upper = text.upper().strip()
        
        # Parse signal type
        signal_type = None
        if text_upper.startswith('BUY'):
            signal_type = 'BUY'
        elif text_upper.startswith('SELL'):
            signal_type = 'SELL'
        elif text_upper.startswith('HOLD'):
            signal_type = 'HOLD'
        else:
            return None
        
        # Extract symbol and price
        parts = text_upper.split()
        
        if len(parts) < 2:
            return None
        
        symbol = parts[1]
        price = None
        
        # Look for price in message
        if 'AT' in parts:
            at_index = parts.index('AT')
            if at_index + 1 < len(parts):
                try:
                    price = float(parts[at_index + 1])
                except ValueError:
                    pass
        
        return {
            'signal': signal_type,
            'symbol': symbol,
            'price': price,
            'raw_text': text,
            'timestamp': datetime.now(),
        }
    
    @staticmethod
    def extract_numbers(text: str) -> list:
        """
        Extract all numbers from text.
        
        Args:
            text: Text to extract from
            
        Returns:
            List of numbers found
        """
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        return [float(n) for n in numbers]
    
    @staticmethod
    def is_trading_signal(text: str) -> bool:
        """
        Check if message contains a trading signal.
        
        Args:
            text: Message text
            
        Returns:
            True if contains trading signal
        """
        signal_keywords = ['BUY', 'SELL', 'HOLD', 'ENTRY', 'EXIT', 'TARGET', 'STOP']
        text_upper = text.upper()
        
        return any(keyword in text_upper for keyword in signal_keywords)
