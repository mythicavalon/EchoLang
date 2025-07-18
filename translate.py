import asyncio
import logging
from googletrans import Translator
import time
import random

logger = logging.getLogger(__name__)

class TranslationService:
    """Service for handling message translations using Google Translate with improved reliability"""
    
    def __init__(self):
        self.translator = None
        self._rate_limit_delay = 2.0  # Increased delay for better stability
        self._last_request_time = 0
        self._retry_attempts = 3
        self._backoff_multiplier = 2
        self._max_text_length = 1000
    
    def _get_translator(self):
        """Get a fresh translator instance for better reliability"""
        try:
            return Translator()
        except Exception as e:
            logger.error(f"Failed to create translator instance: {e}")
            return None
    
    async def translate(self, text, target_language):
        """
        Translate text to target language with retry logic and better error handling
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code (e.g., 'es', 'fr', 'ja')
            
        Returns:
            str: Translated text or descriptive error message
        """
        if not text or not text.strip():
            return "[Empty message]"
        
        # Sanitize and limit text length
        text = text.strip()
        if len(text) > self._max_text_length:
            text = text[:self._max_text_length] + "..."
            
        # Remove potentially problematic characters
        text = self._sanitize_text(text)
        
        for attempt in range(self._retry_attempts):
            try:
                # Rate limiting with jitter
                await self._apply_rate_limit(attempt)
                
                # Perform translation in thread to avoid blocking
                result = await asyncio.get_event_loop().run_in_executor(
                    None, self._translate_sync, text, target_language, attempt
                )
                
                self._last_request_time = time.time()
                
                # Validate translation result
                if result and not self._is_error_result(result):
                    return result
                else:
                    logger.warning(f"Translation attempt {attempt + 1} returned invalid result: {result}")
                    if attempt == self._retry_attempts - 1:
                        return f"[Translation failed - {target_language.upper()}]"
                    
            except Exception as e:
                logger.error(f"Translation attempt {attempt + 1} failed: {e}")
                if attempt == self._retry_attempts - 1:
                    return f"[Translation error - {target_language.upper()}]"
                
                # Wait before retry with exponential backoff
                await asyncio.sleep(self._backoff_multiplier ** attempt + random.uniform(0.1, 0.5))
        
        return f"[Translation unavailable - {target_language.upper()}]"
    
    def _sanitize_text(self, text):
        """Remove or replace problematic characters that might cause translation issues"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove some problematic Unicode characters that might cause issues
        problematic_chars = ['\u200b', '\u200c', '\u200d', '\ufeff']
        for char in problematic_chars:
            text = text.replace(char, '')
        
        return text
    
    def _is_error_result(self, result):
        """Check if the translation result indicates an error"""
        if not result:
            return True
        
        error_indicators = [
            'Translation unavailable',
            'Translation failed',
            'Translation error',
            '[Translation',
            'Error:'
        ]
        
        return any(indicator in result for indicator in error_indicators)
    
    async def _apply_rate_limit(self, attempt):
        """Apply rate limiting with backoff for retries"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        
        # Base delay plus additional delay for retries
        required_delay = self._rate_limit_delay + (attempt * 0.5)
        
        if time_since_last < required_delay:
            sleep_time = required_delay - time_since_last + random.uniform(0.1, 0.3)
            logger.info(f"Rate limiting: waiting {sleep_time:.2f}s (attempt {attempt + 1})")
            await asyncio.sleep(sleep_time)
    
    def _translate_sync(self, text, target_language, attempt):
        """
        Synchronous translation method with improved error handling
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code
            attempt (int): Current attempt number
            
        Returns:
            str: Translated text or error message
        """
        try:
            # Create new translator instance for each attempt
            translator = self._get_translator()
            if not translator:
                return f"[Service unavailable - {target_language.upper()}]"
            
            logger.info(f"Attempting translation to {target_language} (attempt {attempt + 1})")
            
            # Attempt translation with timeout handling
            result = translator.translate(text, dest=target_language)
            
            if result and hasattr(result, 'text') and result.text:
                translated_text = result.text.strip()
                
                # Validate the translation isn't just the same text
                if translated_text.lower() == text.lower() and target_language != 'en':
                    logger.warning(f"Translation returned identical text for {target_language}")
                    return f"[No translation needed - {target_language.upper()}]"
                
                # Add source language info if detected and different
                if (hasattr(result, 'src') and result.src and 
                    result.src != target_language and result.src != 'auto'):
                    source_lang = result.src.upper()
                    return f"{translated_text}\n\n*Detected source: {source_lang}*"
                else:
                    return translated_text
            else:
                logger.error(f"Translation returned empty or invalid result")
                return f"[Translation failed - {target_language.upper()}]"
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific known errors
            if 'timeout' in error_msg or 'connection' in error_msg:
                logger.error(f"Connection/timeout error on attempt {attempt + 1}: {e}")
                return f"[Connection timeout - {target_language.upper()}]"
            elif 'rate limit' in error_msg or '429' in error_msg:
                logger.error(f"Rate limit hit on attempt {attempt + 1}: {e}")
                return f"[Rate limited - {target_language.upper()}]"
            elif 'quota' in error_msg or 'limit exceeded' in error_msg:
                logger.error(f"Quota exceeded on attempt {attempt + 1}: {e}")
                return f"[Quota exceeded - {target_language.upper()}]"
            else:
                logger.error(f"Translation error on attempt {attempt + 1}: {e}")
                return f"[Translation error - {target_language.upper()}]"
    
    async def detect_language(self, text):
        """
        Detect the language of given text with retry logic
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Language code or None if detection fails
        """
        if not text or not text.strip():
            return None
        
        text = self._sanitize_text(text[:500])  # Limit text length for detection
        
        for attempt in range(2):  # Fewer retries for detection
            try:
                await self._apply_rate_limit(attempt)
                
                result = await asyncio.get_event_loop().run_in_executor(
                    None, self._detect_language_sync, text
                )
                
                if result:
                    return result
                    
            except Exception as e:
                logger.error(f"Language detection attempt {attempt + 1} failed: {e}")
                if attempt == 0:
                    await asyncio.sleep(1)  # Brief wait before retry
        
        return None
    
    def _detect_language_sync(self, text):
        """
        Synchronous language detection
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Language code or None
        """
        try:
            translator = self._get_translator()
            if not translator:
                return None
            
            result = translator.detect(text)
            
            if result and hasattr(result, 'lang') and result.lang:
                return result.lang
            else:
                return None
                
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return None
    
    async def get_supported_languages(self):
        """
        Get list of supported languages
        
        Returns:
            dict: Dictionary of language codes and names
        """
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._get_supported_languages_sync
            )
            
            return result or {}
            
        except Exception as e:
            logger.error(f"Error getting supported languages: {e}")
            return {}
    
    def _get_supported_languages_sync(self):
        """
        Synchronous method to get supported languages
        
        Returns:
            dict: Dictionary of language codes and names
        """
        try:
            # Get languages from googletrans
            from googletrans import LANGUAGES
            return LANGUAGES
            
        except Exception as e:
            logger.error(f"Error getting supported languages sync: {e}")
            return {}
    
    def get_service_status(self):
        """
        Get current service status information
        
        Returns:
            dict: Service status information
        """
        return {
            'service': 'Google Translate',
            'rate_limit_delay': self._rate_limit_delay,
            'retry_attempts': self._retry_attempts,
            'max_text_length': self._max_text_length,
            'last_request_time': self._last_request_time
        }
