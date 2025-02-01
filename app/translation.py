from googletrans import Translator  # @ Importing Translator class from googletrans library for translation functionality.

translator = Translator()  # @ Creating an instance of the Translator class.

def translate_text(text: str, target_lang: str) -> str:  # @ Defining the function to translate text into the target language.
    """Translate text to target language using Google Translate."""  # @ Description of the function's purpose.
    try:
        translation = translator.translate(text, dest=target_lang)  # @ Attempting to translate the text to the target language.
        return translation.text  # @ Returning the translated text if successful.
    except Exception as e:  # @ If an error occurs during translation, handle the exception.
        print(f"Translation error: {e}")  # @ Printing the error message.
        return text  # @ Returning the original text as a fallback in case of an error.
