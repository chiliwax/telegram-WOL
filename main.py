import os
import telegram
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import date
from wakeonlan import send_magic_packet
from scapy.all import srp, Ether, ARP
import time

load_dotenv()
# ENV CONSTANTS
BOT_NAME = os.getenv('BOT_NAME')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_AUTHAURIZE_CHANNEL = os.getenv('TELEGRAM_AUTHAURIZE_CHANNEL')
PC_MAC_ADDR = os.getenv('PC_MAC_ADDR')
MACOS_MAC_ADDR = os.getenv('MACOS_MAC_ADDR')
IP_RANGE = os.getenv('IP_RANGE')
RECONNECTION_ATEMPT = os.getenv('RECONNECTION_ATEMPT')

# GLOBALS SET
INPROCESS = False

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
    global INPROCESS 
    if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL) and INPROCESS == False:
        INPROCESS = True
        send_magic_packet(str(PC_MAC_ADDR))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Trying starting PC...')
        for value in range(int(RECONNECTION_ATEMPT)):
            time.sleep(5)
            ip = getIpForMacAddr()
            if ip is not None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'connected on {ip} !')
                INPROCESS = False
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'retrying ({int(RECONNECTION_ATEMPT) - value})...')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'connexion timeout ! wait I use status or retry...')
        INPROCESS = False
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"can't perform this operation now ")

async def status(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL):
        ip = getIpForMacAddr()
        alive = "alive" if ip is not None else "down"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Host : {alive} on {ip}')

async def poweronmac(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    global INPROCESS 
    if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL) and INPROCESS == False:
        INPROCESS = True
        send_magic_packet(str(MACOS_MAC_ADDR))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Trying starting MAC...')
        for value in range(int(RECONNECTION_ATEMPT)):
            time.sleep(5)
            ip = getIpForMacAddr(str(MACOS_MAC_ADDR))
            if ip is not None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'connected on {ip} !')
                INPROCESS = False
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'retrying ({int(RECONNECTION_ATEMPT) - value})...')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'connexion timeout ! wait I use status or retry...')
        INPROCESS = False
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"can't perform this operation now ")

async def statusmac(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == int(TELEGRAM_AUTHAURIZE_CHANNEL):
        ip = getIpForMacAddr(str(MACOS_MAC_ADDR))
        alive = "alive" if ip is not None else "down"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Host : {alive} on {ip}')

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
    application.add_handler(CommandHandler(poweronmac.__name__, poweronmac))
    application.add_handler(CommandHandler(statusmac.__name__, statusmac))
    application.add_handler(CommandHandler(kill.__name__, kill))
    # other commands
    application.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), echo))
    # run the bot
    application.run_polling()
    
# Ip Scanning
def getIpForMacAddr(macAddr = PC_MAC_ADDR):
    # Craft an ARP request packet
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24", hwdst="ff:ff:ff:ff:ff:ff")
    # Send the ARP request and wait for responses
    responses, _ = srp(arp_request, timeout=2, verbose=False)
    # Iterate through responses
    for _, response in responses:
        if response.hwsrc == macAddr.replace(".", ":").lower():
            return response.psrc  # Return the IP address if MAC address matches
    return None  # Return None if MAC address not found
    
    #return ans.summary()

# Life Cycle
def main():
    initLogging()
    runTelegramBot()

if __name__ == "__main__":
    main()
