import os
import telegram
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import date
from wakeonlan import send_magic_packet

load_dotenv()
# ENV CONSTANTS
BOT_NAME = os.getenv('BOT_NAME')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_AUTHAURIZE_CHANNEL = os.getenv('TELEGRAM_AUTHAURIZE_CHANNEL')
PC_MAC_ADDR = os.getenv('PC_MAC_ADDR')

# SYSLOG INSTANCE
logger = logging.getLogger()

# SYSLOG INITIALIZATION
def initLogging(level: int = logging.INFO):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level
    )

# Telegram commands

async def poweron(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
	if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL):
		mgc_pckt = send_magic_packet(str(PC_MAC_ADDR))
		logger.log(logging.INFO, msg=PC_MAC_ADDR)
		logger.log(logging.INFO, msg=mgc_pckt)
		print(PC_MAC_ADDR)
		print(mgc_pckt)
		await context.bot.send_message(chat_id=update.effective_chat.id, text=f'PC IS STARTING')
	pass

async def status(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
	if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL):
		await context.bot.send_message(chat_id=update.effective_chat.id, text=f'STATUS : not implemented yet !')
	pass

async def echo(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'receive {update.message.text}')
    if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Command not recognize')

async def kill():
    exit()

# Telegram bot
def runTelegramBot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    # register commands
    application.add_handler(CommandHandler(poweron.__name__, poweron))
    application.add_handler(CommandHandler(status.__name__, status))
    application.add_handler(CommandHandler(kill.__name__, kill))
    # other commands
    application.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), echo))
    # run the bot
    application.run_polling()

# Life Cycle
def main():
    initLogging()
    runTelegramBot()


if __name__ == "__main__":
    main()
