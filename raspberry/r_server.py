
#!/usr/bin/env python3
#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

from flask import Flask, render_template, jsonify, request, redirect, make_response

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

LED1 = 7 #Définit le numéro du port GPIO qui alimente la led
LED2 = 11 #Définit le numéro du port GPIO qui alimente la led
LED3 = 13 #Définit le numéro du port GPIO qui alimente la led


GPIO.setup(LED1, GPIO.OUT) #Active le contrôle du GPIO
GPIO.setup(LED2, GPIO.OUT) #Active le contrôle du GPIO
GPIO.setup(LED3, GPIO.OUT) #Active le contrôle du GPIO

@app.route("/ouvrir1", methods=["GET"])
def o1():
    state = GPIO.input(LED1) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

    print("Etat", state)
    if state : #Si GPIO allumé
        GPIO.output(LED1, GPIO.LOW) #On l’éteint
        print("Eteint")
        return "{ status: 'eteint'}"
    else : #Sinon
        GPIO.output(LED1, GPIO.HIGH) #On l'allume
        return "{ status: 'allume'}"



@app.route("/ouvrir2", methods=["GET"])
def o2():
    state = GPIO.input(LED2) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

    print("Etat", state)
    if state : #Si GPIO allumé
        GPIO.output(LED2, GPIO.LOW) #On l’éteint
        print("Eteint")
        return "{ status: 'eteint'}"
    else : #Sinon
        GPIO.output(LED2, GPIO.HIGH) #On l'allume
        return "{ status: 'allume'}"



@app.route("/ouvrir3", methods=["GET"])
def o3():
    state = GPIO.input(LED3) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

    print("Etat", state)
    if state : #Si GPIO allumé
        GPIO.output(LED3, GPIO.LOW) #On l’éteint
        print("Eteint")
        return "{ status: 'eteint'}"
    else : #Sinon
        GPIO.output(LED3, GPIO.HIGH) #On l'allume
        return "{ status: 'allume'}"

    

# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

# Si creation du serveur par gunicorn : deploiement depuis Github
def create_app(test_config=None):
  return app
