from telegram import Update
from telegram.ext import ContextTypes
from utils.data_manipulation import UserManager, GreetingsManager, QuizManager

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user

    phrase = GreetingsManager.get_random_phrase()


    if len(phrase.en.split(" ")) == 1:
        game = QuizManager.create_scramble_game(tg_user.id, phrase)
        await update.message.reply_text(game.title)
    else:
        # Button Game
        ...
    
    return
