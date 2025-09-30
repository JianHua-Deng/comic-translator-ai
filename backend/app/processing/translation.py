from googletrans import Translator
import asyncio

class TextTranslator:
    def __init__(self, translator_option='default'):
        self.translator = Translator()

    async def translate(self, text, original_language: str ='ja', target_language: str ='en') -> str:
        try:
            result = await self.translator.translate(text, src=original_language, dest=target_language)
            return result.text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return text # Return original text if translation failed
        
    
    async def translate_batch(self, texts: list, original_language: str = 'ja', target_language: str='en') -> list:

        if not texts:
            return []

        try:
            results = await self.translator.translate(texts, src=original_language, dest=target_language)
            return [result.text.upper() for result in results]
        except Exception as e:
            print(f"An error occurred during batch translation: {e}")
            return texts # Return original text if translation failed
