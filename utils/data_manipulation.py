import json
from config import BASE_DIR
from models.user import User
from datetime import datetime
from typing import Optional, List
from string import ascii_lowercase
from random import choice, shuffle
from models.greetings import Phrase
from models.games import ScrambleGame
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
    def get_user_by_id(cls, id: int) -> Optional[User]:
        users = cls._load()
        for user in users:
            if user.id == id:
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
    def update_user_by_id(cls, id: int, new_data: dict) -> bool:
        users = cls._load()

        for i, user in enumerate(users):
            if user.id == id:
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
        

class QuizManager:

    @staticmethod
    def _load() -> List[ScrambleGame]:
        try:
            with open(f"{BASE_DIR}/data/scramble_games.json", "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            return []

        scramble_games = [ScrambleGame(**sb) for sb in raw_data]
        return scramble_games

    @staticmethod
    def _save(scramble_games: List[ScrambleGame]) -> None:
        with open(f"{BASE_DIR}/data/scramble_games.json", "w", encoding="utf-8") as f:
            json.dump(
                [{**sg.model_dump()} for sg in scramble_games],
                f,
                ensure_ascii=False,
                indent=4
            )

    @classmethod
    def get_active_scramble_game(cls, user_id: int, phrase: Phrase) -> ScrambleGame | None:
        games = cls._load()
        for game in games:
            if game.user_id == user_id and game.is_active:
                return game
        return QuizManager.create_scramble_game(user_id, phrase, games)

    @staticmethod
    def create_scramble_game(user_id: int, phrase: Phrase, games: List[ScrambleGame])-> ScrambleGame:
        user = UserManager.get_user_by_id(id=user_id)
        
        if not user: raise Exception("Xəta oldu! User olmadan bu komanda işləmir!")
        
        
        new_id = 1 if not games else games[-1].id + 1


        while True:
            word = phrase.en.lower()
            letters = [ch for ch in word if ch in ascii_lowercase]
            shuffle(letters)
            scrambled_word = "".join(letters)

            if list(scrambled_word) != [ch for ch in word if ch in ascii_lowercase]:
                break


        title = f"Bu hərflərdən düzgün söz düzəlt: {scrambled_word}"

        new_game = ScrambleGame(
            id=new_id,
            user_id=user_id,
            title=title,
            answer="".join([ch for ch in list(phrase.en.lower()) if ch in ascii_lowercase]),
            score=1
        )

        games.append(new_game)
        QuizManager._save(games)

        
        user.active_game_id = new_game.id 

        data = user.model_dump()
        data.pop("tg_id", None) 
        UserManager.update_user(tg_id=user.tg_id, new_data=data)
        return new_game
 
            