import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! প্রেডিকশন বটে স্বাগতম।")

async def prediction(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    txt = " ".join(ctx.args)
    if not txt:
        await update.message.reply_text("❗ ব্যবহার: /prediction [টেক্সট]")
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ হ্যা", callback_data="yes"), InlineKeyboardButton("❌ না", callback_data="no")]
    ])
    await ctx.bot.send_message(chat_id=update.effective_chat.id, text=txt, reply_markup=kb)

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    resp = "✅ আপনি হ্যা বেছে নিয়েছেন।" if q.data=="yes" else "❌ আপনি না বেছে নিয়েছেন।"
    await q.edit_message_text(f"{q.message.text}\n\n🤖 আপনার চয়েস: {resp}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

