
#!/usr/bin/env python3
#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

from flask import Flask, render_template, jsonify, request, redirect, make_response

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

LED = 7 #Définit le numéro du port GPIO qui alimente la led

GPIO.setup(LED, GPIO.OUT) #Active le contrôle du GPIO

state = GPIO.input(LED) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

print("Etat", state)
if state : #Si GPIO allumé
    GPIO.output(LED, GPIO.LOW) #On l’éteint
    print("Eteint")
else : #Sinon
    GPIO.output(LED, GPIO.HIGH) #On l'allume
    print("Allume")



@app.route("/ouvrir", methods=["GET"])
def home():
    # A faire : allumer diode / ouvrir rack
    return "{ status: 'ok'}"
    # return app.send_static_file('index.html')  # Simplement afficher le fichier index.html

# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(debug=True)

# Si creation du serveur par gunicorn : deploiement depuis Github
def create_app(test_config=None):
  return app
