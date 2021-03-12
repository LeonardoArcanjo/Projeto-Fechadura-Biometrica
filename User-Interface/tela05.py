# Title: Biometric Lock User Interface
# Organization: Optima-UFAM
# Screen 5: Fingerprint Enrolling Calibration Screen
# version: 2.0
# Description: Gets fingerprint data for the member previously enrolled
# Especs: Touchscreen LCD 3,5" 480x320
# Autor: Leonardo Arcanjo
# Review: Leonardo Arcanjo
# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# Exception Handler for Tkinter Package
try:
    # for Python 2.7
    from Tkinter import *
except ImportError:
    # for Pyhton 3
    from tkinter import *

# Screens neighbors
import tela04, tela03
# SQLite Database package
import sqlite3
# Error log package
from logs.ErrorLog import writeError
# time package
from time import sleep
# RPi.GPIO package
import RPi.GPIO as gpio
# Fingerprint package
from pyfingerprint.pyfingerprint import PyFingerprint

LED_RED = 40
LED_GREEN = 38
LED_BLUE = 36

def setup_gpio():
    gpio.setmode(gpio.BOARD)
    gpio.setup(LED_BLUE, gpio.OUT)
    gpio.setup(LED_RED, gpio.OUT)
    gpio.setup(LED_GREEN, gpio.OUT)
    
def turnOn_led(led_pin):
    gpio.output(led_pin, 1)
    
def turnOff_led(led_pin):
    gpio.output(led_pin, 0);

def blink_led(led_pin, times):
    turnOff_led(LED_BLUE)
    
    for i in range(times):
        turnOn_led(led_pin)
        sleep(0.5)
        turnOff_led(led_pin)
        sleep(0.5)

def initialize_sensor():
    try:
        f = PyFingerprint("/dev/ttyUSB0", 57600, 0xFFFFFFFF, 0x00000000)
    
        if(f.verifyPassword() == False):
            raise ValueError("The given fingerprint sensor password is wrong!")

    except Exception as e:
        writeError("Initialize_sensor", str(e))
        blink_led(LED_RED, 1)
    
    return f

def telacinco():
    class ScreenFive:
        def __init__(self, master=None): # constructor class
            # constructor of Layout Frame
            self.firstContainer = Frame(master)
            self.firstContainer["pady"] = 10
            self.firstContainer.pack()
            
            self.secondContainer = Frame(master)
            self.secondContainer["padx"] = 20
            self.secondContainer["pady"] = 5
            self.secondContainer.pack(fill=X, expand=YES)
            
            self.thirdContainer = Frame(master)
            self.thirdContainer["padx"] = 20
            self.thirdContainer.pack()
            
            # First Container Elements
            self.title = Label(self.firstContainer)
            self.title["text"] = "Fingerprint Enroll"
            self.title["font"] = ("Arial", "20", "bold")
            self.title.pack()
            
            # Second Container Elements
            self.prompt = Text(self.secondContainer)
            self.prompt["relief"] = FLAT
            self.prompt["height"] = 10
            self.prompt.pack()
            
            fontButtons = ("Arial", "12")
            
            # Third Container Elements
            self.returnButton = Button(self.thirdContainer)
            self.returnButton["text"] = "RETURN"
            self.returnButton["font"] = fontButtons
            self.returnButton["command"] = return_screenFour
            self.returnButton["width"] = 10
            self.returnButton.pack(side = LEFT)
            
            self.runButton = Button(self.thirdContainer)
            self.runButton["text"] = "ENROLL"
            self.runButton["font"] = fontButtons
            self.runButton["command"] = self.enroll_fingerprint
            self.runButton["width"] = 10
            self.runButton.pack(side = LEFT)
            
            self.okButton = Button(self.thirdContainer)
            self.okButton["text"] = "OK"
            self.okButton["font"] = fontButtons
            self.okButton["width"] = 10
            self.okButton["command"] = conclude
            self.okButton.pack(side = LEFT)
            
            setup_gpio()
        
        def __str__(self):
            return "tela05.py"
    
        def enroll_fingerprint(self):
            self.prompt.insert(END, "Initializing the Sensor...\n")
            self.prompt.update()
            
            sensor = initialize_sensor()
            
            if sensor is None:
                self.prompt.insert(END, "Sensor not Connected\n")
            else:
                self.prompt.insert(END, "Sensor Connected\n")
            
            self.prompt.update()
            
            try:
                self.prompt.insert(END, "Waiting for finger... \n")
                turnOn_led(LED_BLUE)
                self.prompt.update()
                
                while(sensor.readImage() == False):
                    pass
                
                self.prompt.insert(END, "Remove finger\n")
                turnOff_led(LED_BLUE)
                self.prompt.update()
                
                sleep(2)
                
                sensor.convertImage(0x01)
                
                answer = sensor.searchTemplate()
                positionNumber = answer[0]
                
                if (positionNumber >= 0):
                    self.prompt.insert(END, "Template already exists at position: " + str(positionNumber) + "\n")
                    blink_led(LED_RED, 2)
                    self.prompt.insert(END, "Enrolled other finger")
                    self.prompt.update()
                    del sensor
                    sleep(2)
                    root.destroy()
                    telacinco()
                
                self.prompt.insert(END, "Waiting for same finger...\n")
                turnOn_led(LED_BLUE)
                self.prompt.update()
                
                while(sensor.readImage() == False):
                    pass
                
                self.prompt.insert(END, "Remove finger...\n")
                turnOff_led(LED_BLUE)
                self.prompt.update()
                
                sleep(2)
                
                sensor.convertImage(0x02)
                
                if(sensor.compareCharacteristics() == 0):
                    self.prompt.insert(END, "Fingers don't match!!\n")
                    self.prompt.update()
                    blink_led(LED_RED, 3)
                    del sensor
                    
                sensor.createTemplate()
                positionNumber = sensor.storeTemplate()
                
                blink_led(LED_GREEN, 2)
                
                self.prompt.insert(END, "Fingers match!!!\n")
                self.prompt.update()
                del sensor
                
                url = "/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db"
                conn = sqlite3.connect(url)
                cursor = conn.cursor()
                
                try:
                    cursor.execute("""
                                    ALTER TABLE optima
                                    ADD COLUMN pos_number INTEGER""")
                    cursor.execute("""
                                    UPDATE optima
                                    SET pos_number = (?)
                                    WHERE pos_number IS NULL """, (positionNumber,))
                except:
                    cursor.execute("""
                                    UPDATE optima
                                    SET pos_number = (?)
                                    WHERE pos_number IS NULL""", (positionNumber,))
                    
                conn.commit()
                conn.close()
                self.prompt.insert(END, "User successfully enrolled!!\n")
                self.prompt.update()
                
            except Exception as e:
                writeError(str(ScreenFive.__str__), str(e))
                blink_led(LED_RED, 4)
                del sensor
            except UnboundLocalError:
                writeError(str(ScreenFive.__str__), "Sensor was deleted")
                blink_led(LED_RED, 4)
    
    
    def conclude(): # Invokes the Screen Three
        root.destroy()
        tela03.telatres()
        
    def return_screenFour(): # Invokes the Screen Four
        try: # Try to clear the user from DB that not enrolled its fingerprint
            conn = sqlite3.connect("/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db")
            cursor = conn.cursor()
            
            cursor.execute("""SELECT * FROM optima WHERE pos_number is ?""", (None))
            
            row = cursor.fetchall()
            index = row[0]
            index = index[0]
            
            cursor.execute("DELETE FROM optima WHERE member_id is ?", (index,))
            conn.commit()
            conn.close()
        
        except Exception as e:
            writeError(str(ScreenFive.__str__), str(e))
        
        root.destroy()
        tela04.telaquatro()
            
    root = Tk()
    ScreenFive(root)
    root.title("Fingerprint Enroll screen")
    root.geometry("478x320")
    root.attributes("-fullscreen", True)
    root.mainloop()
    

if __name__ == "__main__":
    telacinco()