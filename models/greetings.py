from pydantic import BaseModel


class Phrase(BaseModel):
    id: int
    
    en: str
    az: str
