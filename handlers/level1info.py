from telegram import Update
from telegram.ext import ContextTypes
from utils.data_manipulation import GreetingsManager

async def level_1_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phrases = GreetingsManager.get_phrases()

    if not phrases:
        await update.message.reply_text("Heç bir ifadə tapılmadı 😅")
        return
    else:
        msg_lines = [f"№ {ph.id}\n{ph.en}\n{ph.az}" for ph in phrases]
        msg = "--- İfadələr ---\n" + "\n\n".join(msg_lines)
        msg += "\n\n/play yazaraq oyuna başla"

        await update.message.reply_text(msg)