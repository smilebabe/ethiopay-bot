import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token from @BotFather
TOKEN = 8175654585:AAHkKi9IVa1C0vCknGHQ9ildFgsiwXvmXG4,

# Forex rates (update daily)
FOREX_RATES = {
    "black_market": 57.5,
    "bank_rate": 56.3,
    "our_rate": 57.2,
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
}

# Predefined responses
RESPONSES = {
    "paypal": """💰 *3 Legal Ways to Access PayPal in Ethiopia:*

1️⃣ *Through Family Abroad* (Most Common)
   • Family member receives to their PayPal
   • Transfers to their bank
   • Sends you via Telebirr/Bank
   📊 *Fees:* 2-5%

2️⃣ *Payoneer Bridge Method*
   • Create Payoneer account
   • Receive to Payoneer USD account
   • Withdraw to Ethiopian bank
   📊 *Fees:* 1.8-2.5%

3️⃣ *Direct Bank Transfer* (High Loss)
   • Client sends via bank wire
   • Bank converts at official rate
   • You receive 15-25% less
   📊 *Fees:* 20-30%

📱 *Need step-by-step guide?*
Send 'GUIDE' or click /guide""",

    "upwork": """🎯 *How to Get Paid from Upwork in Ethiopia:*

*Method 1: Payoneer (Recommended)*
1. Create Payoneer account (free)
2. Add to Upwork as payout method
3. Withdraw to your Ethiopian bank
   ⚡ *Processing:* 2-3 days
   💰 *Fees:* 2% + bank charges

*Method 2: Direct Local Transfer*
1. Client pays via Upwork
2. Choose "Direct to Local Bank"
3. Enter your CBE/BoA account
   ⚡ *Processing:* 5-7 days
   💰 *Fees:* $30 flat + 1.5%

*Method 3: Wise (if available)*
1. Get Wise USD account details
2. Receive to Wise
3. Convert to ETB and send
   ⚡ *Processing:* 1-2 days
   💰 *Fees:* 0.5-1%

🔗 *Connect with verified agent for setup:* /agent""",

    "rate": f"""📈 *Today's Forex Rates ({FOREX_RATES['updated']})*

• *Black Market:* $1 = {FOREX_RATES['black_market']} ETB
• *Bank Rate:* $1 = {FOREX_RATES['bank_rate']} ETB
• *Our Network:* $1 = {FOREX_RATES['our_rate']} ETB ✅

*Why our rate is better:*
✓ Verified agents only
✓ Escrow protection
✓ 24/7 support
✓ No advance payment

💰 *Need to exchange?* /agent""",

    "scam": """⚠️ *10 Forex Scams Targeting Ethiopians:*

1. "Pay 50% upfront" ❌
2. No physical office address ❌
3. Fake WhatsApp business accounts ❌
4. Too good to be true rates (e.g., $1 = 60 ETB) ❌
5. Pressure tactics ("last chance") ❌
6. No verifiable client testimonials ❌
7. Asking for ID card photos early ❌
8. Unregistered Telegram channels ❌
9. "Western Union/MoneyGram only" ❌
10. No escrow system ❌

✅ *Our Verified Agents:*
✓ Registered businesses
✓ Client references available
✓ Escrow protection
✓ Max 10% commission
✓ Physical office visit possible

🔒 *Connect with safe agents:* /agent""",

    "fiverr": """🎨 *Fiverr Payments to Ethiopia:*

*Recommended Path:*
1. Fiverr → Payoneer → Local Bank
   • Lowest fees (1.8%)
   • Fastest (2-3 days)
   • Most reliable

*Step-by-Step:*
1. Sign up for Payoneer (free)
2. Verify with passport/ID
3. Connect to Fiverr Revenue Card
4. Withdraw to your bank account

*Alternative:* Wise → Bank (if available)

📚 *Full tutorial video:* Available in Premium Group (2000 ETB/month)
Join: /join""",

    "guide": """📖 *The Ultimate Ethiopian Freelancer Payment Guide*
*Price:* 500 ETB (One-time)

*What's inside:*
✅ 47-page PDF with screenshots
✅ Step-by-step setup for 5 platforms
✅ Tax calculation templates
✅ Legal compliance checklist
✅ Agent verification checklist
✅ Sample client contracts

*How to get it:*
1. Send 500 ETB via Telebirr to *0912-345-6789*
2. Send screenshot to this bot
3. Receive guide instantly

💡 *Bonus:* First 100 buyers get free 15-min consultation!

Click 'PAYMENT PROOF' below after payment.""",

    "agent": """🤝 *Connect with Verified Forex Agent*

*Available Agents:*
1️⃣ *Addis Forex Solutions* (Addis)
   • Rate: $1 = 57.1 ETB
   • Min: $100
   • Commission: 9%
   • Contact: @AddisForexAgent

2️⃣ *Safe Transfer Ethiopia* (Online)
   • Rate: $1 = 57.0 ETB
   • Min: $50
   • Commission: 8.5%
   • Contact: @SafeTransferET

3️⃣ *Diaspora Bridge* (US/Canada focus)
   • Rate: $1 = 57.3 ETB
   • Min: $200
   • Commission: 10%
   • Contact: @DiasporaBridge

⚠️ *Always use escrow!* Never pay 100% upfront.

Need help choosing? Describe your needs:
• Amount in USD: ______
• Location: ______
• Urgency: ______"""
}

# Command handlers
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💰 PayPal Solutions", callback_data='paypal')],
        [InlineKeyboardButton("🎯 Upwork/Fiverr", callback_data='upwork')],
        [InlineKeyboardButton("📈 Forex Rates", callback_data='rate')],
        [InlineKeyboardButton("⚠️ Avoid Scams", callback_data='scam')],
        [InlineKeyboardButton("📖 Buy Guide (500 ETB)", callback_data='guide')],
        [InlineKeyboardButton("🤝 Connect Agent", callback_data='agent')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"""🤖 *Welcome to EthioPay Bot!*

*I solve payment problems for Ethiopians getting paid abroad.*

*Ask me about:*
• Receiving PayPal/Stripe/Wise money
• Upwork/Fiverr payments
• Best forex rates
• Avoiding scams
• Legal tax compliance
• Finding verified agents

*Or use buttons below for instant answers!*

📢 *Join our communities:*
• @EthioFreelancers (Jobs)
• @RemoteWorkEthiopia (Opportunities)
• @DiasporaToEthiopia (Send money)

💎 *Premium Support:* /join
        """,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        """*Available Commands:*

/start - Start the bot
/rates - Current forex rates
/guide - Get payment guide (500 ETB)
/agent - Connect with verified agents
/join - Join premium group (2000 ETB/month)
/report - Report scam agent

*Or just type your question!*
Examples:
• "How to get PayPal money?"
• "Best rate for $1000?"
• "Is this agent legit?"
• "Fiverr payment method"

📢 *Daily tips:* @EthioPayments""",
        parse_mode='Markdown'
    )

async def rates(update: Update, context: CallbackContext):
    await update.message.reply_text(
        RESPONSES['rate'],
        parse_mode='Markdown'
    )

async def guide(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("✅ I've Paid (Send Screenshot)", callback_data='paid')],
        [InlineKeyboardButton("📞 Need Help?", url='https://t.me/EthioPaySupport')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        RESPONSES['guide'],
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def agent(update: Update, context: CallbackContext):
    await update.message.reply_text(
        RESPONSES['agent'],
        parse_mode='Markdown'
    )

async def join(update: Update, context: CallbackContext):
    await update.message.reply_text(
        """💎 *Premium Group Benefits (2000 ETB/month)*

✅ *Daily Features:*
• Live rate alerts (6 AM, 12 PM, 6 PM)
• New agent verification reports
• Tax law updates
• Job leads from abroad

✅ *Weekly Features:*
• Group Q&A with experts
• Contract review (1 page free)
• Success story interviews

✅ *Monthly Features:*
• Free guide updates
• Priority agent matching
• 15-min 1-on-1 consultation

*How to join:*
1. Send 2000 ETB via Telebirr to *0961393003*
2. Forward payment screenshot here
3. Get instant invitation to @EthioPayPremium

*Money-back guarantee:* First 3 days 100% refund if not satisfied.""",
        parse_mode='Markdown'
    )

# Handle button presses
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data in RESPONSES:
        await query.edit_message_text(
            text=RESPONSES[query.data],
            parse_mode='Markdown'
        )
    elif query.data == 'paid':
        await query.edit_message_text(
            text="""✅ *Payment Received!*

Please send your payment screenshot to @EthioPaySupport.

*You'll receive within 5 minutes:*
1. PDF Guide download link
2. Bonus templates
3. Invitation to buyers' group

*Thank you for your purchase!* 🎉""",
            parse_mode='Markdown'
        )

# Handle text messages
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    
    # Keyword matching
    if any(word in text for word in ['paypal', 'pay pal', 'stripe']):
        response = RESPONSES['paypal']
    elif any(word in text for word in ['upwork', 'up work']):
        response = RESPONSES['upwork']
    elif any(word in text for word in ['fiverr', 'fiveer']):
        response = RESPONSES['fiverr']
    elif any(word in text for word in ['rate', 'forex', 'birr', 'dollar']):
        response = RESPONSES['rate']
    elif any(word in text for word in ['scam', 'fake', 'fraud', 'trust']):
        response = RESPONSES['scam']
    elif any(word in text for word in ['guide', 'book', 'pdf', 'tutorial']):
        response = RESPONSES['guide']
    elif any(word in text for word in ['agent', 'broker', 'exchange', 'change']):
        response = RESPONSES['agent']
    elif any(word in text for word in ['hello', 'hi', 'hey']):
        response = "👋 Hello! Ask me about getting paid from abroad, forex rates, or avoiding scams!"
    else:
        response = """🤔 *I understand you're asking about:* "{}"

*Here's what I can help with:*
• Payment methods from abroad 💰
• Current forex rates 📈
• Avoiding scams ⚠️
• Finding verified agents 🤝
• Tax compliance 📋

*Try these commands:*
/rates - Latest forex rates
/guide - Step-by-step payment guide
/agent - Connect with agents

*Or be more specific like:*
"How to receive PayPal money?"
"What's today's dollar rate?"
"Need agent for $500 exchange\"""".format(text)
    
    # Add footer to every response
    footer = "\n\n📢 *For daily tips:* @EthioPayments\n💎 *Premium support:* /join"
    
    await update.message.reply_text(
        response + footer,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

# Error handler
async def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rates", rates))
    application.add_handler(CommandHandler("guide", guide))
    application.add_handler(CommandHandler("agent", agent))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    # Start the bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':

    main()
