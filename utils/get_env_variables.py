import os 
from dotenv import load_dotenv

load_dotenv()

def get_tbt()->str:
    token = os.getenv("TG_BOT_TOKEN", None)
    if not token: 
        raise Exception("Token tapılmadı və ya xəta oldu!")
    return token 