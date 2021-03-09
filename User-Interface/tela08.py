"""
#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 10: Check-in Screen
#Description: Check-in Screen for the User Interface
#Especs: Touchscreen LCD 3,5" 480x320
#Author: Leonardo Arcanjo
#Review: Leonardo Arcanjo
"""
# !/usr/local/bin/python
# -*- coding: uft-8 -*-

# Tkinter Package Exception Handling
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import sqlite3
import tela01
import time
import os
from datetime import datetime

import RPi.GPIO as gpio
from pyfingerprint.pyfingerprint import PyFingerprint

# Defines GPIO pins connect to RGB LED and Eletric Magnetic Lock
LED_RED = 40
LED_GREEN = 38
LED_BLUE = 36
LOCK_PIN = 32


def acendeLed(pino_led):
    gpio.output(pino_led, 1)
    return


def apagaLed(pino_led):
    gpio.setmode(gpio.BOARD)
    gpio.setup(pino_led, gpio.OUT)
    gpio.output(pino_led, 0)
    return


def telaoito():
    class ScreenEight:
        def __init__(self, master=None):
            self.widget1 = Frame(master)
            self.widget1["pady"] = 10
            self.widget1.pack()

            self.widget2 = Frame(master)
            self.widget2["padx"] = 10
            self.widget2.pack()

            self.titulo = Label(self.widget1, text="Check-in Screen")
            self.titulo["font"] = ("Arial", "20", "bold")
            self.titulo.pack()

            self.texto = Text(self.widget2)
            self.texto["relief"] = SUNKEN
            self.texto["height"] = 15
            self.texto.pack()

            configura_GPIO()  # Sets the Raspberry Pi GPIO
            self.texto.insert(END, "Initializing the sensor\n")
            self.widget2.after(1000, self.connectSensor)  # this method calls the funcion connectSensor after 1 second.

        def connectSensor(self):
            # this function tries to connect the Fingerprint sensor e shows message of confirmation or not
            global f
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
                self.showMessage("Sensor Connect\n")
            except Exception as e:
                print('Exception message: ' + str(e))
                self.showMessage("Sensor not connected\n")
                self.showMessage("Error: " + str(e) + "\n")
               # self.widget2.after(2000, fechar)
                os.system("reboot") 

            self.showMessage("Waiting for finger...\n")
            acendeLed(LED_BLUE)  # acende o LED azul
            
            try:
                positionIndex = readSensor()
            except Exception as e:
                self.showMessage(str(e) + '\n')
                self.showMessage("Rebooting...")
                os.system('reboot')

            if positionIndex == -1:
                self.showMessage("No match found!!!\n")
                self.showMessage("Try again...\n")
                pisca_led(LED_RED)
                self.connectSensor()
            else:
                pisca_led(LED_GREEN)
                nome = DBAcess(positionIndex)
                self.showMessage(nome)
                unlockDoor()
                self.widget2.after(3000, fechar)

        def showMessage(self, mensagem):
            self.texto.insert(END, mensagem)

    def DBAcess(index):
        # this function connects optima DB and searches the user associated to fingerprint index,
        # salves the user's entry in Stream.txt file and returns first name and lastname user's as string
        conn = sqlite3.connect("/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT
                    first_name AS FIRST_NAME,
                    last_name AS LAST_NAME,
                    title AS TITLE
                    FROM optima WHERE pos_number=?""", (str(index)))
        rows = cursor.fetchall()

        conn.commit()
        conn.close()

        for row in rows:
            continue

        now = datetime.now()
        hora = now.strftime("%d/%m/%Y %H:%M:%S")
        with open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Stream.txt', 'a') as arquivo:
            arquivo.writelines(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + hora + " Entrada\n")

        with open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Control.txt', 'a') as file_control:
            file_control.writelines(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + "\n")

        return str(row[0] + " " + row[1])

    def pisca_led(pin):
        """Blinks the LED that's associate to pin parameter"""
        apagaLed(LED_BLUE)
        acendeLed(pin)
        time.sleep(0.5)
        apagaLed(pin)
        time.sleep(0.5)
        acendeLed(pin)
        time.sleep(0.5)
        apagaLed(pin)

    def fechar():  #
        """ Destroys the current screen and calls Tela01.py"""
        apagaLed(LED_BLUE)
        gpio.cleanup()
        root.destroy()
        tela01.telaum()

    def configura_GPIO():
        """Sets GPIO as BOARD mode and LEDS pins as OUTPUT"""
        gpio.setmode(gpio.BOARD)
        gpio.setup(LED_RED, gpio.OUT)
        gpio.setup(LED_GREEN, gpio.OUT)
        gpio.setup(LED_BLUE, gpio.OUT)

    def readSensor():
        """ Reads fingerprint sensor and returns index user from sensor """
        i = 0
        while f.readImage() is False:
            if i == 1400:
                fechar()
            i = i + 1
            pass
        f.convertImage(0x01)
        try:
            result = f.searchTemplate()
            return result[0]
        except:
            print("Serial Communication lost")
            gpio.cleanup()
            root.destroy()
            tela01.telaum()

    def unlockDoor():
        """Set Electric Lock pin as OUTPUT and sends a signal to unlock the door"""
        gpio.setup(LOCK_PIN, gpio.OUT)
        gpio.output(LOCK_PIN, 1)
        time.sleep(0.5)
        gpio.output(LOCK_PIN, 0)
        time.sleep(0.5)
        gpio.cleanup()

    # Tkinter object instance
    root = Tk()
    ScreenEight(root)
    root.title("Check-in Screen")
    root.geometry("478x320")
    root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == "__main__":
    telaoito()
