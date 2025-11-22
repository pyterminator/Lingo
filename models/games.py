from pydantic import BaseModel

class ScrambleGame(BaseModel):
    id: int
    user_id: int 
    title: str 
    answer: str 
    score: int 
    is_active: bool = True
