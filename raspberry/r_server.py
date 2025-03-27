
#!/usr/bin/env python3
#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

from flask import Flask, render_template, jsonify, request, redirect, make_response

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

LED = 7 #Définit le numéro du port GPIO qui alimente la led

GPIO.setup(LED, GPIO.OUT) #Active le contrôle du GPIO



@app.route("/ouvrir", methods=["GET"])
def home():
    state = GPIO.input(LED) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

    print("Etat", state)
    if state : #Si GPIO allumé
        GPIO.output(LED, GPIO.LOW) #On l’éteint
        print("Eteint")
        return "{ status: 'eteint'}"
    else : #Sinon
        GPIO.output(LED, GPIO.HIGH) #On l'allume
        return "{ status: 'allume'}"

    

# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

# Si creation du serveur par gunicorn : deploiement depuis Github
def create_app(test_config=None):
  return app
