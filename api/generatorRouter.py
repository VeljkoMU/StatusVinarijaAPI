
from datetime import datetime
from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from custom_logger import CustomLogger
from userRouter import User, authenticate_token
from email.message import Message
import logging
import string
from tokenize import String
from turtle import update

from telegram import Update, ForceReply
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


generator_args_parser = reqparse.RequestParser()
generator_args_parser.add_argument("time", type=str)
#Funkcije koje zeljko treab da napravi pocinju slovom Z

class Generator(Resource):

    logger = CustomLogger()

    def get(self, genNum, token):
        #Ovde se pribavljaju infomracije o generatoru (stanje senzora1 i senzora2 i da li se generator puni ili prazni)
        #state je promenjiva koja cuva stanja, ovo treba da vrati Zeljkova funkcija koja cita stanja generatora
        state = {
            "senzor1": False,
            "senzor2": True,
            "stanje": "neutralno"
        }

        #state = ZgetSenzorData(genNum)
        return make_response(jsonify(state), 200)
        
    def post(self, genNum, token):
        if not authenticate_token(token)[0] or (authenticate_token(token)[2][0]!="upravljac" and authenticate_token(token)[2][0]!="administrator"):
            return Response(None, 405)

        time = generator_args_parser.parse_args()['time']
        name = authenticate_token(token)[2][1]
        #post metoda koja scheduluje pravnjenje za navedeni generator
        #Ovde se poziva Zeljkov kod koji scheduluje da se izvrsi punujenje i praznjenje
        if not time:
            return Response(None, 403)
        if not Generator.logger.check_availability(time):
            return Response(None, 403)

        print(time)
        pt = datetime(int(time[0:4]),int(time[5:7]), int(time[8:10]), int(time[11:13]), int(time[14:]))
        print(pt)
        isSuccsessful = True
        #Zeljko, ova funkcija treab da vraca True ako je uspesno zakazano praznjenje i punjenje
        #isSuccsessful = ZzakaziOperaciju(genNum, time)
        if isSuccsessful:
            Generator.logger.enter_log(time, name)
            return Response(None, 200)
        else:
            return Response(None, 500)

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

def telegram_main() -> None:
    """Start the bot."""
    updater = Updater("5113828696:AAGP9deAAz_wkzlHpprfV6jbjHtwpcvRQWU")


    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, stanje))

    updater.start_polling()
    updater.idle()
    