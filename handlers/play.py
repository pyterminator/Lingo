from telegram import Update
from telegram.ext import ContextTypes
from utils.data_manipulation import UserManager, GreetingsManager, QuizManager

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    user = UserManager.get_user_by_tg_id(tg_id=tg_user.id)

    if user and user.active_game_id:
        await update.effective_chat.delete_message(message_id=update.message.id)
        return 
    
    phrase = GreetingsManager.get_random_phrase()
    if len(phrase.en.split(" ")) == 1:
        game = QuizManager.get_active_scramble_game(user.id, phrase)
        await update.message.reply_text(game.title)
    else:
        print(phrase.en)
        ...
    
    return
