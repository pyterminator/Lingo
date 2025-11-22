from telegram import Update
from telegram.ext import ContextTypes
from utils.data_manipulation import UserManager

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user

    user_data = {
        "tg_id": tg_user.id,
        "is_bot": tg_user.is_bot,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
        "language_code": tg_user.language_code,
        "is_premium": getattr(tg_user, "is_premium", False),
    }

    user = UserManager.add_user(user_data)
    
    await update.message.reply_text(
        f"Qeydiyyatınız uğurla tamamlanmışdır ✅\nSizin level: {user.level}\nSizin xalınız: {user.score}\n/level1info yazaraq level 1-in ifadələrinə bax"
    )
