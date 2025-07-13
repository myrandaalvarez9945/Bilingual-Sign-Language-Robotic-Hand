from deep_translator import GoogleTranslator

def translate_text(text, language="EN"):
    if language == "EN":
        src, tgt = "en", "es"
    else:
        src, tgt = "es", "en"

    try:
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return text  # fallback to original if error

def translate_to_sign_language(text, language="EN"):
    if not text:
        return ""

    translated = translate_text(text, language)
    return f"{'ASL' if language == 'EN' else 'LSE'}: {translated.upper()}"