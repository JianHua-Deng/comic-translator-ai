from googletrans import Translator as GoogleTranslator
import translators as ts
import asyncio

class TextTranslator:
    def __init__(self, translator_option='default'):
        self.translate_engine = translator_option
        if translator_option == 'google':
            self.translator = GoogleTranslator()
        else:
            self.translator = ts

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

            if self.translate_engine == 'google':
                results = await self.translator.translate(texts, src=original_language, dest=target_language)
                return [result.text.upper() for result in results]
            else:
                tasks = [ asyncio.to_thread(self.translator.translate_text,  t, from_language=original_language, to_language=target_language, translator='google') for t in texts]
                results = await asyncio.gather(*tasks)
                print(results)
                return(getattr(r, 'text', str(r)).upper() for r in results)
            
        except Exception as e:
            print(f"An error occurred during batch translation: {e}")
            return texts # Return original text if translation failed
