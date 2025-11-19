from googletrans import Translator as GoogleTranslator
import translators as ts
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Gemini if available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class TextTranslator:
    def __init__(self, translator_option='gemini'):
        self.translate_engine = translator_option

        if translator_option == 'gemini' and GEMINI_AVAILABLE:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print("Warning: GEMINI_API_KEY not found. Falling back to Google Translate.")
                self.translate_engine = 'google'
                self.translator = GoogleTranslator()
            else:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("models/gemini-2.0-flash")
                print("Using Gemini: gemini-2.0-flash")

        elif translator_option == 'google':
            self.translator = GoogleTranslator()
            print("Using Google Translate")
        else:
            self.translator = ts
            print("Using Translators library")

    async def translate(self, text, original_language: str ='ja', target_language: str ='en') -> str:
        try:
            if self.translate_engine == 'gemini':
                prompt = f"""Translate the following Japanese manga text to English.

Rules:
- Translate naturally, preserving the tone and emotion
- Keep it concise for speech bubbles
- Preserve sound effects in a natural English equivalent
- Return ONLY the translated text, no explanations

Text to translate: {text}"""

                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt
                )
                translation = response.text.strip()
                return translation
            else:
                result = await self.translator.translate(text, src=original_language, dest=target_language)
                return result.text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return text # Return original text if translation failed
        
    
    async def translate_batch(self, texts: list, original_language: str = 'ja', target_language: str='en') -> list:

        if not texts:
            return []

        try:
            if self.translate_engine == 'gemini':
                # Translate each text individually for better reliability
                print(f"[Gemini] Translating {len(texts)} texts individually...", flush=True)

                translations = []
                for i, text in enumerate(texts):
                    try:
                        prompt = f"""Translate this Japanese manga text to English. Keep it concise for speech bubbles.

Japanese text: {text}

Return ONLY the English translation in UPPERCASE, nothing else."""

                        response = await asyncio.to_thread(
                            self.model.generate_content,
                            prompt
                        )

                        translation = response.text.strip().replace('**', '').replace('*', '').upper()
                        translations.append(translation)
                        print(f"[Gemini] {i+1}/{len(texts)}: '{text[:30]}...' -> '{translation[:30]}...'", flush=True)

                    except Exception as e:
                        print(f"[Gemini] Error translating text {i+1}: {e}", flush=True)
                        translations.append(text.upper())

                return translations

            elif self.translate_engine == 'google':
                results = await self.translator.translate(texts, src=original_language, dest=target_language)
                return [result.text.upper() for result in results]
            else:
                tasks = [asyncio.to_thread(self.translator.translate_text, t, from_language=original_language, to_language=target_language, translator='google') for t in texts]
                results = await asyncio.gather(*tasks)
                print(results)
                return [getattr(r, 'text', str(r)).upper() for r in results]

        except Exception as e:
            print(f"An error occurred during batch translation: {e}")
            return texts # Return original text if translation failed
