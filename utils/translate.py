from googletrans import Translator


def tercume_et(en: str)-> str:
    if not isinstance(en, str):
        raise Exception("Tərcümə etmək üçün mətn göndər!")
    
    translator = Translator()
    result = translator.translate(en, src="en", dest="az")
    return result.text