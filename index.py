import asyncio
from utils.db import init_db
from telegram.ext import ApplicationBuilder
from utils.get_env_variables import get_tbt


async def main():
    token = get_tbt()
    await init_db()

    app = ApplicationBuilder().token(token).build()

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())


    