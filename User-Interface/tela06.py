"""
# Title: Biometric Lock User Interface#for
# Organization: Optima-UFAM
# Screen 5: Member Deleting Screen
# Description: Shows list of enrolled member for admin level user to delete one of them from database
# INPUTS: optima.db
# Especs: Touchscreen LCD 3,5" 480x320
# Autor: Diego Vieira
# Review: Leonardo Arcanjo
# Revision: Leonardo Arcanjo
"""
# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# Tkinker Package Exception Handling
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import messagebox
# importa bibliotecas utilizadas pelos metodos da classe

from pynput.keyboard import (Key, Controller)
import sqlite3
from pyfingerprint.pyfingerprint import PyFingerprint  # from pyfingerprint(package) pyfingerprint(module)
# import Pyfingerprint(Class)
# importa telas que interagem com tela atual
import tela03


def telaseis():
    class ScreenSix:
        def __init__(self, master=None):  # Class

            # layout em formato de grid
            self.primeiroContainer = Frame(master)
            self.primeiroContainer.grid(row=0, column=0,
                                        rowspan=2, columnspan=2, sticky=NW)

            # Listbox Attributes
            self.lista = Listbox(self.primeiroContainer, width=30, height=10,
                                 font=('MS', '13'), selectmode=BROWSE)
            self.scroll = Scrollbar(self.primeiroContainer, command=self.lista.yview)
            self.lista.configure(yscrollcommand=self.scroll.set)
            self.lista.pack(side=LEFT)
            self.scroll.pack(side=RIGHT, fill=Y)

            self.fontePadrao = ("Arial", "10")

            # UP Button Attributes
            self.BotaoUp = Button(master, text='UP', font=self.fontePadrao,
                                  width=19, height=7, command=ScrollUp)
            self.BotaoUp.grid(row=0, column=2, sticky=NW)

            # DOWN Button Attributes
            self.BotaoDown = Button(master, text='DOWN', font=self.fontePadrao,
                                    width=19, height=6, command=ScrollDown)
            self.BotaoDown.grid(row=1, column=2, sticky=NW)

            # LOAD Button Attributes
            self.BotaoLoad = Button(master, text='LOAD', font=self.fontePadrao,
                                    width=20, height=6, command=self.fetch_data)
            self.BotaoLoad.grid(row=2, column=0, sticky=SW)

            # BACK Button Attributes
            self.BotaoBack = Button(master, text="BACK", font=self.fontePadrao,
                                    width=21, height=6, command=backtoenroll)
            self.BotaoBack.grid(row=2, column=1, sticky=SW)

            # DELETE Button Attributes
            self.BotaoDelete = Button(master, text="DELETE", font=self.fontePadrao,
                                      width=20, height=6, command=self.run_listbox_delete)
            self.BotaoDelete.grid(row=2, column=2, sticky=SW)
	    # running db reading in screen
            self.fetch_data()


        def run_listbox_delete(self):
            """Calls listbox_data_delete() if messagebox.askyesno() method return True"""
            answer = messagebox.askyesno("Confirmation", "Are you sure you want to delete?")
            if answer:
                self.listbox_data_delete()

        def listbox_data_delete(self):
            """Lists the users present in DB, get user index to use in deletar() function"""
            items = self.lista.curselection()
            pos = 0
            for i in items:
                idx = int(i) - pos
                self.deletar(idx)
                pos += 1

        def deletar(self, number):
            """Deletes User in DB and listbox"""
            database_data_delete(number)
            self.lista.delete(number)

        def fetch_data(self):  # database query main loop
            conn = sqlite3.connect(
                '/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db')  # instancia o banco de dados
            cursor = conn.cursor()
            cursor.execute("""SELECT
                               first_name AS FIRST_NAME,
                               last_name AS LAST_NAME,
                               title AS TITLE,
                               admin AS ADMIN_LEVEL,
                               pos_number AS POSITION_NUMBER
                           FROM optima""")
            rows = cursor.fetchall()

            self.lista.delete(0, END)  # essa funcao serve para deletar tudo que aparece na scroll bar

            for row in rows:
                self.lista.insert(END, row)

            self.lista.focus_set()

    def ScrollDown():
        keyboard = Controller()
        keyboard.press(Key.down)
        keyboard.release(Key.down)

    def ScrollUp():
        keyboard = Controller()
        keyboard.press(Key.up)
        keyboard.release(Key.up)

    def database_data_delete(numIdx):
        "# This function deletes the user in DB from numIdx is passed as argument"
        conn = sqlite3.connect('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT member_id FROM optima ORDER BY member_id ASC;""")

        row = cursor.fetchall()  # This method returns a tuple list with the member_id's
        vetor = []
        i = 0

        # for loop to take the tuples content and organize them in a list
        for numero in row:
            vetor.insert(i, numero[0])
            i += 1

        cursor.execute("""SELECT pos_number, last_name FROM optima WHERE member_id=?""", (vetor[numIdx],))
        indSensor = cursor.fetchall()

        vetor_aux = []
        i = 0

        # for loop to take the only content of tuple list that's the Sensor index that it'll delete
        # on Sensor memory
        for indexSen in indSensor:
            for j in indexSen:
                vetor_aux.insert(i, indexSen[i])
                i += 1

        try:
            apagaIndex(int(vetor_aux[0]))  # Deleting the fingerprint by Index in Sensor
            cursor.execute("""DELETE FROM optima WHERE member_id=?""", (vetor[numIdx],))
        except TypeError:
            cursor.execute("""DELETE FROM optima WHERE last_name=?""", (vetor_aux[1],))
        finally:
            conn.commit()
            conn.close()

    def apagaIndex(indexSensor):
        # This function deletes the indicated indexSensor when it's passed as argument
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if f.verifyPassword() is False:
                raise ValueError('The given fingerprint sensor password is wrong!')
            try:
                if f.deleteTemplate(indexSensor):
                    print('Index Apagado!')
            except Exception as e:
                print('Operacao falhou')
                print('Excecao: ' + str(e))

        except Exception as e:
            print('The Fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            # tentando fazer um loop pra tentar reiniciar a conexão com o sensor
            del f
            apagaIndex(indexSensor)

    def fechar():
        root.destroy()

    def backtoenroll():
        fechar()
        tela03.telatres()

    # Tkinter Object Instance
    root = Tk()
    ScreenSix(root)
    root.title("Delete Screen")
    root.geometry('478x320')
    root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == "__main__":  # permite executar esse script como principal
    telaseis()
