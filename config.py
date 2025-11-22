import os 
from dotenv import load_dotenv

# Load_dotenv
load_dotenv()

# BASE_DIR
BASE_DIR = os.getcwd() 



def get_tbt()->str:
    token = os.getenv("TG_BOT_TOKEN", None)
    if not token: 
        raise Exception("Token tapılmadı və ya xəta oldu!")
    return token 