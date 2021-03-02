"""
#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 4: Enroll Screen
#Description: Screen for enroll a brand new lab member, allows admin level user confirm data before upload to database
#INPUTS: Name; Title; Button for Fingerprint Loop
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#Review: Leonardo Arcanjo
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
# imports python packages that are used by ScreenFour Class methods
import hashlib
import logging
import sqlite3

# Imports
import tela01
import tela05

# Creates Sqlite file
conn = sqlite3.connect('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db')
cursor = conn.cursor()

# Formates Table in DB
cursor.execute("""CREATE TABLE IF NOT EXISTS optima (
            member_id integer PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            title TEXT NOT NULL,
            admin integer,
            senhas TEXT NOT NULL,
            UNIQUE (first_name, last_name))""")
conn.commit()
conn.close()


def telaquatro():
    class ScreenFour:
        def __init__(self, master=None):  # Class
            self.primeiroContainer = Frame(master)
            self.primeiroContainer.grid(row=0, column=0, rowspan=6, columnspan=3, sticky=NW)

            fontePadrao = ("Arial", "12")

            # First Container Attributes
            self.firstnameLabel = Label(self.primeiroContainer)
            self.firstnameLabel["text"] = "First Name"
            self.firstnameLabel["font"] = fontePadrao
            self.firstnameLabel.grid(row=0, column=0, padx=10, pady=3, sticky=NW)

            self.firstname = Entry(self.primeiroContainer)
            self.firstname["width"] = 24
            self.firstname["font"] = fontePadrao
            self.firstname.grid(row=0, column=1, padx=0, pady=3, sticky=NW)

            self.lastnameLabel = Label(self.primeiroContainer)
            self.lastnameLabel["text"] = "Last Name"
            self.lastnameLabel["font"] = fontePadrao
            self.lastnameLabel.grid(row=1, column=0, padx=10, pady=3, sticky=NW)

            self.lastname = Entry(self.primeiroContainer)
            self.lastname["width"] = 24
            self.lastname["font"] = fontePadrao
            self.lastname.grid(row=1, column=1, padx=0, pady=3, sticky=NW)

            self.titleLabel = Label(self.primeiroContainer)
            self.titleLabel["text"] = "Title\t"
            self.titleLabel["font"] = fontePadrao
            self.titleLabel.grid(row=2, column=0, padx=10, pady=3, sticky=NW)

            self.title = Entry(self.primeiroContainer)
            self.title["width"] = 24
            self.title["font"] = fontePadrao
            self.title.grid(row=2, column=1, padx=0, pady=3, sticky=NW)

            self.passwordLabel = Label(self.primeiroContainer)
            self.passwordLabel["text"] = "Password"
            self.passwordLabel["font"] = fontePadrao
            self.passwordLabel.grid(row=3, column=0, padx=10, pady=0, sticky=NW)

            self.password = Entry(self.primeiroContainer)
            self.password["width"] = 24
            self.password["font"] = fontePadrao
            self.password["show"] = "*"
            self.password.grid(row=3, column=1, padx=0, pady=0, sticky=NW)

            self.var = IntVar()
            self.check = Checkbutton(self.primeiroContainer)
            self.check["font"] = fontePadrao
            self.check["text"] = "Admin"
            self.check["variable"] = self.var
            self.check.grid(row=2, column=2, padx=0, pady=0, sticky=NW)

            self.botaoLoad = Button(self.primeiroContainer)
            self.botaoLoad["text"] = "LOAD"
            self.botaoLoad["font"] = fontePadrao
            self.botaoLoad["command"] = self.showinput
            self.botaoLoad["width"] = 22
            self.botaoLoad.grid(row=4, column=1, padx=0, pady=0, sticky=NW)

            self.msg = Message(self.primeiroContainer)
            self.msg["text"] = "First Name: \nLast Name: \nTitle: \nAdmin:"
            self.msg["relief"] = SUNKEN
            self.msg.grid(row=5, column=1, padx=0, pady=0, sticky=NW)

            self.botaoMainMenu = Button(self.primeiroContainer)
            self.botaoMainMenu["text"] = "MAIN MENU"
            self.botaoMainMenu["width"] = 10
            self.botaoMainMenu["height"] = 4
            self.botaoMainMenu["command"] = returntohome
            self.botaoMainMenu.grid(row=6, column=0, padx=0, pady=0, sticky=NW)

            self.botaoCancel = Button(self.primeiroContainer)
            self.botaoCancel["text"] = "CANCEL"
            self.botaoCancel["width"] = 25
            self.botaoCancel["height"] = 4
            self.botaoCancel["command"] = self.eraseinput
            self.botaoCancel.grid(row=6, column=1, padx=0, pady=0, sticky=NW)

            self.botaoFingerprint = Button(self.primeiroContainer)
            self.botaoFingerprint["text"] = "FINGERPRINT"
            self.botaoFingerprint["width"] = 15
            self.botaoFingerprint["height"] = 4
            self.botaoFingerprint["command"] = self.enabledb
            self.botaoFingerprint.grid(row=6, column=2, padx=0, pady=0, sticky=NW)

        def showinput(self):
            # Get attributes from user
            p_first_name = self.firstname.get()
            p_last_name = self.lastname.get()
            p_title = self.title.get()
            p_admin = self.var.get()
            

            if p_first_name != "" and p_last_name != "":
                if p_admin == 1:
                    self.msg[
                        "text"] = "First Name: " + p_first_name + "\nLast Name: " + p_last_name + "\nTitle: " + p_title + "\nAdmin: YES"
                    
                    p_password = self.password.get()
                    self.botaoLoad["state"] = DISABLED
                
                else:
                    self.msg[
                        "text"] = "First Name: " + p_first_name + "\nLast Name: " + p_last_name + "\nTitle: " + p_title + "\nAdmin: NO"
                    self.botaoLoad["state"] = DISABLED
            
            else:
                
                self.msg["text"] = "First Name: \nLast Name: \nTitle: \nAdmin:"

        def eraseinput(self):  # metodo que apaga a entrada digitada - comandado pelo botao CANCEL
            p_first_name = self.firstname.get()
            p_last_name = self.lastname.get()
            p_title = self.title.get()
            p_admin = self.var.get()

            self.msg["text"] = "First Name: \nLast Name: \nTitle: \nAdmin:"
            
            if p_admin == 1:
                self.check.toggle()
                
            self.firstname.delete(0, END)
            self.lastname.delete(0, END)
            self.title.delete(0, END)
            self.password.delete(0, END)
            
            del p_first_name
            del p_last_name
            del p_title
            del p_admin
            
            self.botaoFingerprint["state"] = NORMAL
            self.botaoLoad["state"] = NORMAL

        def enabledb(self):
            """Inserts the data input by user in DB"""
            # get info by user on entry input
            p_first_name = self.firstname.get()
            p_last_name = self.lastname.get()
            p_title = self.title.get()
            p_password = self.password.get()
            p_admin = self.var.get()

            pfirstname = p_first_name.casefold()
            plastname = p_last_name.casefold()
            
            if(pfirstname == "") and (plastname == ""):
                self.msg["text"] = "Please, Type a valid data"
                raise Exception("InvalidAttributeError")

            # Exception Handling to verify copies
            try:
                p_password = p_password.encode('utf-8')
                p_password = hashlib.sha256(p_password).hexdigest()
                # escreve valores no banco
                conn = sqlite3.connect('optima.db')
                cursor = conn.cursor()

                if p_admin == 1:
                    cursor.execute("""
                        INSERT INTO optima (first_name, last_name, title, admin, senhas)
                        VALUES (?, ?, ?, ?, ?)
                        """, (pfirstname, plastname, p_title, p_admin, p_password)
                                   )
                else:
                    cursor.execute("""
                        INSERT INTO optima (first_name, last_name, title, admin)
                        VALUES (?, ?, ?, ?)
                        """, (pfirstname, plastname, p_title, p_admin)
                                   )
                conn.commit()
                conn.close()
                root.destroy()

                # creating custom logger
                logger = logging.getLogger(__name__)
                # handler setting
                f_handler = logging.FileHandler('datalog.txt')
                f_handler.setLevel(logging.DEBUG)
                # setting format
                f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -- %(message)s',
                                             '%d/%m/%Y %H:%M:%S')
                f_handler.setFormatter(f_format)
                # Add loggers to the handler
                logger.addHandler(f_handler)

                if p_admin == 1:
                    logger.info("First Name: %s \tLast Name: %s \tTitle: %s \tAdmin:YES", p_first_name, p_last_name,
                                p_title)
                if p_admin == 0:
                    logger.info("First Name: %s \tLast Name: %s \tTitle: %s \tAdmin:NO", p_first_name, p_last_name,
                                p_title)

                tela05.telacinco()

            except sqlite3.Error as e:  # se o python levantar uma excecao - ocorre esse loop
                erro = ' '.join(e.args)
                
                erro = erro.split(" ")
                
                if erro[0] == 'UNIQUE':
                    self.msg["text"] = "Name already enrolled. Input new data."
                else:
                    self.msg["text"] = ' '.join(erro)
                
                self.botaoLoad["state"] = DISABLED
                self.botaoFingerprint["state"] = DISABLED
                self.check.toggle()
                
                self.firstname.delete(0, END)
                self.lastname.delete(0, END)
                self.password.delete(0, END)
                self.title.delete(0, END)
                    
                del p_first_name
                del p_last_name
                del p_title
                del p_password
                del p_admin
                
                self.botaoFingerprint["state"] = NORMAL
                self.botaoLoad["state"] = NORMAL
                    

    def returntohome():
        """Destroys current screen and calls tela01 module"""
        root.destroy()
        tela01.telaum()

    # Tkinter object instance
    root = Tk()
    ScreenFour(root)
    root.title("Enroll Screen")
    root.geometry('478x270')
    root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == "__main__":  # permite executar esse script como principal
    telaquatro()
