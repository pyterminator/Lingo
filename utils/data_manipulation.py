import json
from config import BASE_DIR
from models.user import User
from datetime import datetime
from typing import Optional, List
from models.greetings import Phrase
from random import choice

class UserManager:

    @staticmethod
    def _load() -> List[User]:
        try:
            with open(f"{BASE_DIR}/data/users.json", "r", encoding="utf-8") as f:
                raw_users = json.load(f)
        except FileNotFoundError:
            return []

        users = []
        for u in raw_users:
            if "added_at" in u and isinstance(u["added_at"], str):
                u["added_at"] = datetime.fromisoformat(u["added_at"])
            users.append(User(**u))
        return users

    @staticmethod
    def _save(users: List[User]) -> None:
        with open(f"{BASE_DIR}/data/users.json", "w", encoding="utf-8") as f:
            json.dump(
                [
                    {**u.model_dump(), "added_at": u.added_at.isoformat()} 
                    for u in users
                ],
                f,
                ensure_ascii=False,
                indent=4
            )


    @classmethod
    def get_users(cls) -> List[User]:
        return cls._load()

    @classmethod
    def get_user_by_tg_id(cls, tg_id: int) -> Optional[User]:
        users = cls._load()
        for user in users:
            if user.tg_id == tg_id:
                return user
        return None

    @classmethod
    def add_user(cls, data: dict) -> User:
        users = cls._load()

        if any(u.tg_id == data.get("tg_id") for u in users):
            return cls.get_user_by_tg_id(data["tg_id"])

        next_id = max([u.id for u in users], default=0) + 1

        new_user = User(id=next_id, **data)
        users.append(new_user)

        cls._save(users)
        return new_user

    @classmethod
    def update_user(cls, tg_id: int, new_data: dict) -> bool:
        users = cls._load()

        for i, user in enumerate(users):
            if user.tg_id == tg_id:
                updated = user.model_copy(update=new_data)
                users[i] = updated
                cls._save(users)
                return True

        return False

    @classmethod
    def delete_user(cls, tg_id: int) -> bool:
        users = cls._load()
        new_users = [u for u in users if u.tg_id != tg_id]

        if len(users) == len(new_users):
            return False

        cls._save(new_users)
        return True


class GreetingsManager:

    @staticmethod
    def _load() -> List[Phrase]:
        try:
            with open(f"{BASE_DIR}/local-data/greetings.json", "r", encoding="utf-8") as f:
                raw_phrases = json.load(f)
        except FileNotFoundError:
            return []

        phrases = [Phrase(**ph) for ph in raw_phrases]
        return phrases
    
    @classmethod
    def get_phrases(cls) -> List[Phrase]:
        return cls._load()
    
    @classmethod
    def get_phrase_by_id(cls, id: int) -> Optional[Phrase]:
        phrases = cls._load()
        for ph in phrases:
            if ph.id == id:
                return ph
        return None 
    
    @classmethod
    def get_random_phrase(cls)-> Optional[Phrase]:
        phrases = cls._load()
        if not phrases: return None
        return choice(phrases)
        
