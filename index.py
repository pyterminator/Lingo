from config import get_tbt
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from handlers.start import start
from handlers.level1info import level_1_info



if __name__ == "__main__":
    token = get_tbt()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("level1info", level_1_info))
    app.run_polling()