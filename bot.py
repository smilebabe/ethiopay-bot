import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get token from Railway environment
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    print("❌ ERROR: No TOKEN found!")
    print("Please set TOKEN in Railway variables")
    exit(1)

print(f"✅ Bot starting with token: {TOKEN[:15]}...")

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💰 PayPal Solutions", callback_data='paypal')],
        [InlineKeyboardButton("📈 Forex Rates", callback_data='rate')],
        [InlineKeyboardButton("📖 Buy Guide", callback_data='guide')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 Welcome to EthioPay Bot!\n\nHow can I help?",
        reply_markup=reply_markup
    )

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'paypal':
        await query.edit_message_text("💰 PayPal solutions coming soon!")
    elif query.data == 'rate':
        await query.edit_message_text("📈 Today's rate: $1 = 57.5 ETB")
    elif query.data == 'guide':
        await query.edit_message_text("📖 Guide: Send 500 ETB to 0961-393-003 via Telebirr")

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if 'hi' in text or 'hello' in text:
        await update.message.reply_text("Hello! Use /start for menu")
    elif 'rate' in text:
        await update.message.reply_text("Today: $1 = 57.5 ETB")
    else:
        await update.message.reply_text("Try /start for options")

def main():
    print("🚀 Starting bot...")
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot started successfully!")
    
    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
