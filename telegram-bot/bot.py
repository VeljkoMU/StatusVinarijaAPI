from email.message import Message
import logging
import string
from tokenize import String
from turtle import update

from telegram import Update, ForceReply
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Pozdrav {user.mention_markdown_v2()}\!\n dobrodosao u StatusVinarijaBot\nDa proverite stanje odredjenog generatora, ukucajte komandu:\n stanje generatora \<BROJ_GENERATORA\>\n gde cete umesto \<BROJ_GENERATORA\> staviti odgovarajuci redni broj',
        reply_markup=ForceReply(selective=True),
    )

def stanje(update: Update, context: CallbackContext) -> None:
    if "stanje" not in  update.message.text.lower():
        update.message.reply_text("Komanda nije prepoznata")
        return

    genNum = [int(s) for s in update.message.text.split() if s.isdigit()][0]
    print(genNum)
    stanje = {
        "senzor1": True,
        "senzor2": False,
        "stanje": "puni se"
    }

    #stanje = ZVratiStanje(genNum)
    s1 = stanje["senzor1"]
    s2 = stanje["senzor2"]
    s3 = stanje["stanje"]

    msg = f"Generator:{genNum}\nSenzor1:{'Akrivan' if s1 else 'Neaktivan'}\nSenzor2:{'Akrivan' if s2 else 'Neaktivan'}\nStanje:{s3}"
    update.message.reply_text(msg)

def main() -> None:
    """Start the bot."""
    updater = Updater("5113828696:AAGP9deAAz_wkzlHpprfV6jbjHtwpcvRQWU")


    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, stanje))

    updater.start_polling()
    updater.idle()


main()