from telegram import Update
from telegram.ext import ContextTypes
from utils.data_manipulation import UserManager, GreetingsManager

async def level_1_info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    phrases = GreetingsManager.get_phrases()

    msg = "--- İfadələr ---"

    for ph in phrases:
        msg += f"\n№ {ph.id}\n{ph.en}\n{ph.az}\n"
    
    msg += "\n/play yazaraq oyuna başla"

    await update.message.reply_text(msg)