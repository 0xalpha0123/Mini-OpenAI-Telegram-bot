from loguru import logger as log
from openai.error import RateLimitError
from telegram import Update
from telegram.ext import ContextTypes

from loader import config
from openai_api import openai_request


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me any prompt to get OpenAI answer.")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id in map(int, config.TELEGRAM_USERS):
        log.trace(f"Received a prompt: {update.message.text}")
        response = openai_request(prompt=update.message.text)
        log.trace(f"Received a response: {response}")

        try:
            await update.message.reply_html(
                f"<b>{update.message.text}</b> {openai_request(prompt=update.message.text)}"
            )
        except RateLimitError as e:
            log.error(e)
            await update.message.reply_html(f"Something went wrong:\n<code>{e}</code>")

    else:
        log.trace(f"User {update.effective_user.id} not in the list of allowed users")
        await update.message.reply_text("Access denied!")