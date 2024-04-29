import os
import telegram
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import date
from wakeonlan import send_magic_packet
import scanip.scanip as ipScanner
from scapy.all import srp, Ether, ARP

load_dotenv()
# ENV CONSTANTS
BOT_NAME = os.getenv('BOT_NAME')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_AUTHAURIZE_CHANNEL = os.getenv('TELEGRAM_AUTHAURIZE_CHANNEL')
PC_MAC_ADDR = os.getenv('PC_MAC_ADDR')
IP_RANGE = os.getenv('IP_RANGE')

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
    
# Ip Scanning
def getIpForMacAddr():
    # Craft an ARP request packet
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24", hwdst="ff:ff:ff:ff:ff:ff")
    # Send the ARP request and wait for responses
    responses, _ = srp(arp_request, timeout=2, verbose=False)
    # Iterate through responses
    for _, response in responses:
        if response.hwsrc == PC_MAC_ADDR.replace(".", ":"):
            return response.psrc  # Return the IP address if MAC address matches
    return None  # Return None if MAC address not found
    
    #return ans.summary()

# Life Cycle
def main():
    initLogging()
    #runTelegramBot()
    logger.log(logging.INFO, f"ip -> {getIpForMacAddr()}")

if __name__ == "__main__":
    main()
