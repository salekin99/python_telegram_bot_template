import os
import json
import logging
from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (filters, ApplicationBuilder, ContextTypes,
                          CommandHandler, MessageHandler, CallbackQueryHandler,
                          InlineQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# reads your token from environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")


# the function that runs when /start is sent to the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id,
                                   """Hi I'm a telegram bot template! """)


# the function that recieves text messages from users
async def recieve_message(update: Update, context):
    if update.effective_chat.type != 'private':  # there's the inline mode for groups
        return
    await update.message.reply_text(
        text='say something??',
        reply_to_message_id=update.message.message_id,
        parse_mode="HTML")


# recieves the keyboard button clicks
async def get_keyboad_reply(update: Update, context, optional_pram=None):
    chat_id = update.effective_chat.id
    message = update.callback_query.data


# recieves voice messages
async def get_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio_file = await context.bot.get_file(update.message.voice.file_id)
    await audio_file.download_to_drive(update.message.voice.file_id + '.ogg')
    await context.bot.send_message(update.effective_chat.id, 'listening...')


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    if query == '':
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='some item',
            input_message_content=InputTextMessageContent('item_data'))
    ]
    await update.inline_query.answer(results)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(
        CallbackQueryHandler(get_keyboad_reply, block=False))
    application.add_handler(
        CommandHandler(['start', 'help'], start, block=False))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND),
                       recieve_message,
                       block=False))
    application.add_handler(MessageHandler(filters.VOICE, get_voice))
    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling()
