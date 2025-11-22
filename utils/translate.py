from deep_translator import GoogleTranslator

def tercume_et(en: str) -> str:
    if not isinstance(en, str):
        raise Exception("Tərcümə üçün mətin göndərməlisən!")
    return GoogleTranslator(source='en', target='az').translate(en)