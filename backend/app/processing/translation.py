from googletrans import Translator as GoogleTranslator
import google.generativeai as genai
from openai import OpenAI
import asyncio
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TextTranslator:
    def __init__(self):

        self.GoogleTranslator = GoogleTranslator()

        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.GeminiTranslator = genai.GenerativeModel("models/gemini-2.0-flash")
        else:
            self.GeminiTranslator = None
            print("Gemini API Key missing. Gemini translation disabled.")


        deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
        if deepseek_key:
            self.DeepseekTranslatorClient = OpenAI(
                api_key=deepseek_key, 
                base_url="https://api.deepseek.com"
            )
        else:
            self.DeepseekTranslatorClient = None
            print("DeepSeek API Key missing. DeepSeek translation disabled.")



    async def translate_batch(self, texts: list, translator_option: str, original_language: str = 'ja', target_language: str='en') -> list:

        if not texts:
            return []

        try:
            if translator_option == 'gemini' and self.GeminiTranslator:
                return await self.gemini_translation(texts, original_language, target_language)
            
            elif translator_option == "deepseek" and self.DeepseekTranslatorClient:
                return await self.deepseek_translation(texts, original_language, target_language)

            else:
                results = await self.GoogleTranslator.translate(texts, src=original_language, dest=target_language)
                return [result.text.upper() for result in results]

        except Exception as e:
            print(f"An error occurred during batch translation: {e}")
            return texts # Return original text if translation failed
        

        
    async def gemini_translation(self, texts: list, original_language: str, target_language: str):

        print(f"[Gemini] Attempting batch translation for {len(texts)} lines...", flush=True)

        try:

            prompt = f"""
            You are a professional manga translator. Translate the following list of Japanese text to English.
            
            INPUT:
            {json.dumps(texts, ensure_ascii=False)}

            REQUIREMENTS:
            1. Return a JSON list of strings.
            2. The list MUST have exactly {len(texts)} items.
            3. Maintain the exact order of the input.
            4. Keep translations concise for speech bubbles.
            5. Use UPPERCASE for all translations.
            6. Clean up punctuation for display fonts.

            Example Output Format:
            ["HELLO", "GOODBYE", "WHERE IS IT?"]
            """

            response = await asyncio.to_thread(
                self.GeminiTranslator.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )


            translations = json.loads(response.text)


            if not isinstance(translations, list) or len(translations) != len(texts):
                raise ValueError(f"Batch length mismatch: Expected {len(texts)}, got {len(translations)}")

            print(f"[Gemini] Batch success! Translated {len(translations)} lines.", flush=True)
            return translations

        except Exception as e:
            print(f"[Gemini] Batch translation failed ({e}). Switching to individual translation...", flush=True)
            return texts
            # return await self._gemini_fallback(texts)


    async def deepseek_translation(self, texts: list, original_language: str = 'ja', target_language: str = 'en'):

        print(f"[DeepSeek] Attempting batch translation for {len(texts)} lines...", flush=True)

        try:

            prompt = f"""
            Translate the following list of Japanese manga text to English.
            
            INPUT:
            {json.dumps(texts, ensure_ascii=False)}

            REQUIREMENTS:
            1. Return a JSON Object with a single key "translations".
            2. The value of "translations" must be a list of strings.
            3. The list must have exactly {len(texts)} items.
            4. Maintain the exact order.
            5. Text must be UPPERCASE and concise.
            
            Example Output:
            {{
                "translations": ["HELLO", "GOODBYE"]
            }}
            """

            response = await asyncio.to_thread(
                self.DeepseekTranslatorClient.chat.completions.create,
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful manga translator that outputs valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"} 
            )

            content = response.choices[0].message.content
            data = json.loads(content)
            translations = data.get("translations", [])

            if not isinstance(translations, list) or len(translations) != len(texts):
                raise ValueError(f"Batch length mismatch: Expected {len(texts)}, got {len(translations)}")

            print(f"[DeepSeek] Batch success! Translated {len(translations)} lines.", flush=True)
            return translations

        except Exception as e:
            print(f"[DeepSeek] Batch failed ({e})", flush=True)




    '''
    async def translate(self, text, original_language: str ='ja', target_language: str ='en') -> str:
        try:
            if self.translate_engine == 'gemini':
                prompt = f"""
                Translate the following Japanese manga text to English.

                Rules:
                - Translate naturally, preserving the tone and emotion
                - Keep it concise for speech bubbles
                - Preserve sound effects in a natural English equivalent
                - Return ONLY the translated text, no explanations

                Text to translate: {text} """

                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt
                )
                translation = response.text.strip()
                return translation
            else:
                result = await self.translator.translate(text, src=original_language, dest=target_language)
                print(result)
                return result.text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return text # Return original text if translation failed
    '''
