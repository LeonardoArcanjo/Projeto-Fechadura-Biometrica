"""
Title: Biometric Lock User Interface
# Organization: Optima-UFAM
# Screen 1: Main Screen
# Description: Main Screen for the User Interface
# Especs: Touchscreen LCD 3,5" 480x320
# Autor: Diego Vieira
# Review: Leonardo Arcanjo
# Version: 1.0
"""
# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# Tkinter Package Exception Handling
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import RPi.GPIO as GPIO  # Raspberry Pi GPIO Package
# Other Screens Python Module
import tela02
import tela08
import tela10

# Defines switch GPIO
BUTTON_ENTRY = 37


def telaum():
    class ScreenOne:
        def __init__(self, master=None):  # Layout constructor
            self.widget1 = Frame(master)
            self.widget1.pack(fill=X)

            fontePadrao = ('Arial', '24')

            # OPTION button Tkinter attributes
            self.button1 = Button(self.widget1)
            self.button1["text"] = "OPTIONS"
            self.button1["font"] = fontePadrao
            self.button1["height"] = 4
            self.button1["command"] = screen2
            self.button1.pack(side=TOP, fill=X)

            # OPEN THE DOOR button tkinter attributes
            self.button2 = Button(self.widget1)
            self.button2["text"] = "OPEN THE DOOR"
            self.button2["font"] = fontePadrao
            self.button2["height"] = 5
            self.button2["command"] = openDoor
            self.button2.pack(side=TOP, fill=X)

            configura_GPIO()  # Set GPIO Function
        
        def __str__(self):
            return "Tela01.py"

    # Functions
    def screen2():
        """
        Destroys current Screen and calls teladois class in tela02 python module
        """
        root.destroy()
        tela02.teladois()

    def openDoor():
        """
        Destroys current Screen and calls telaoito class in tela08 python module
        """
        root.destroy()
        tela08.telaoito()

    def configura_GPIO():
        """
        Sets Raspberry Pi pin as GPIO mode and Input
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BUTTON_ENTRY, GPIO.IN)

    def checkButton():
        """Every 200 milliseconds, verifies if BUTTON_ENTRY status, by GPIO.input() method. If the method returns TRUE,
            the current screen is destroyed and tela10 module is called. Otherwise, the function runs a loop"""
        if GPIO.input(BUTTON_ENTRY):
            root.destroy()
            tela10.teladez()

        root.after(200, checkButton)

    # Tkinter attributes instance
    root = Tk()
    ScreenOne(root)
    root.title("Main Screen")
    root.geometry('478x320')
    root.overrideredirect(True)  # Instruct the OS window manage ignore this widget.
    # So, minimize, restore and close buttons are hide to user.
    root.after(200, checkButton)  # Entries in check button status loop.
    root.mainloop()


if __name__ == "__main__":  # permite executar esse script como principal
    telaum()
