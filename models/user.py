from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: int
    tg_id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
    added_at: datetime = Field(default_factory=datetime.utcnow)
    active_game_id: Optional[int] = None
    level: int = 1
    score: int = 0