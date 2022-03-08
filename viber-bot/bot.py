
#Prvo doradi:
#pip install flask
#pip install viberbot

import threading
import time
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from sched import scheduler

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='StatusVinarijaBot',
    avatar='',
    auth_token='TOKEN'
))

def setWebhook(bot):
    bot.set_webhook('NAS URL ZA WEBHOOK')

def parse_msg(msg):
    ret = "error"
    if "procitaj statuse generatora" in msg:
        genNum = [int(s) for s in msg.split() if s.isdigit()]
        if(len(genNum)==1):
            #Zeljo treba ovo da vrati:
            #{
            #   senzor1: true ili false
            #   senzor2: true ili false
            #   stanje: puni/prazni/neutralno
            # }
            status= ZgetStanjeGeneratora(numGen[0])
            s1= status["senzor1"]
            s2 = status["senzor2"]
            stanje = status["stanje"]
            ret = f"senzor1= {s1}, senzor2= {s2}, stanje generatora= {stanje}"
    #Ovde idu ostale poruke na koje e da odgovara
    return ret

@app.route('/', methods=['POST'])
def incoming():
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        #Izdvaja se poruka i senderid kome odgovaramo
        msg = viber_request.message
        cId = viber_request.sender.id
        #Analizira se poruka i salej se odgovor (OVDE STAVLAJMO VIBER ENDPOINTE)
        response = parse_msg(msg)
        if response != "error":
            viber.send_message(cId, response)
        else:
            viber.send_message(cId, "Komanda nije prepoznata.")


    return Response(status=200)

if __name__ == "__main__":
    #Webhook ide na poseban thread
    s = scheduler(time.time, time.sleep)
    s.enter(5,1,setWebhook,(viber))
    t=threading.Thread(target=scheduler.run)
    t.start()
    #URL za server kolko sam provalio ne sme da bude isti kao URL za webhook
    app.run(host='HOST URL ZA NAS SERVER', port=8000, debug=True)