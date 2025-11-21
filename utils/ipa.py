import eng_to_ipa as ipa


async def teleffuzu_hazirla(en: str)-> str:
    
    if not isinstance(en, str):
        raise Exception("Tələffüzü hazırlamaq üçün mətn göndərməlisən!")
     
    return ipa.convert(en)