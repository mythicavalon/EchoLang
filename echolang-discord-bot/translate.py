import asyncio
import logging
from googletrans import Translator
import time

logger = logging.getLogger(__name__)

class TranslationService:
    """Service for handling message translations using Google Translate"""
    
    def __init__(self):
        self.translator = Translator()
        self._rate_limit_delay = 1.0  # Increased delay for stability
        self._last_request_time = 0
    
    async def translate(self, text, target_language):
        """
        Translate text to target language
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code (e.g., 'es', 'fr', 'ja')
            
        Returns:
            str: Translated text or error message
        """
        if not text or not text.strip():
            return "[Empty message]"
        
        try:
            # Rate limiting - wait before making request
            current_time = time.time()
            time_since_last = current_time - self._last_request_time
            if time_since_last < self._rate_limit_delay:
                await asyncio.sleep(self._rate_limit_delay - time_since_last)
            
            # Perform translation in thread to avoid blocking
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._translate_sync, text, target_language
            )
            
            self._last_request_time = time.time()
            return result
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"Translation unavailable (Language: {target_language})"
    
    def _translate_sync(self, text, target_language):
        """
        Synchronous translation method
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code
            
        Returns:
            str: Translated text
        """
        try:
            # Limit text length to prevent issues
            if len(text) > 1000:
                text = text[:1000] + "..."
            
            # Create new translator instance for thread safety
            translator = Translator()
            
            # Detect source language and translate
            result = translator.translate(text, dest=target_language)
            
            if result and hasattr(result, 'text') and result.text:
                # Clean up the translated text
                translated_text = result.text.strip()
                
                # Add source language info if detected
                if hasattr(result, 'src') and result.src and result.src != target_language:
                    source_lang = result.src.upper()
                    return f"{translated_text}\n\n*Detected source: {source_lang}*"
                else:
                    return translated_text
            else:
                return f"Translation failed (Language: {target_language})"
                
        except Exception as e:
            logger.error(f"Sync translation error: {e}")
            return f"Translation unavailable (Language: {target_language})"
    
    async def detect_language(self, text):
        """
        Detect the language of given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Language code or None if detection fails
        """
        try:
            if not text or not text.strip():
                return None
                
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._detect_language_sync, text
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return None
    
    def _detect_language_sync(self, text):
        """
        Synchronous language detection
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Language code
        """
        try:
            # Limit text length
            if len(text) > 500:
                text = text[:500]
            
            result = self.translator.detect(text)
            
            if result and result.lang:
                return result.lang
            else:
                return None
                
        except Exception as e:
            logger.error(f"Sync language detection error: {e}")
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
            
            return result
            
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
