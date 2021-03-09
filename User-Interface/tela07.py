"""
# Title: Biometric Lock User Interface
# Organization: Optima-UFAM
# Screen 8: Checkout Screen
# Description: Screen to check who is inside the lab and wants to leave.
# Especs: Touchscreen LCD 3,5" 480x320
# Autor: Leonardo Arcanjo
# Revison: Leonardo Arcanjo
"""
# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# Tkinter Package Exception Handling
try:
    # for python2
    from Tkinter import *
except ImportError:
    # for python3
    from tkinter import *

from pynput.keyboard import Key, Controller
import RPi.GPIO as gpio
import time
from datetime import datetime
import tela01

LOCK_PIN = 32  # GPIO connect to Electric Magnetic Lock


def telasete():
    # vetores de apoio para armazenamento das pessoas que estao no datalog
    vetor_nome = []
    vetor_sobrenome = []
    vetor_cargo = []

    class ScreenSeven:
        def __init__(self, master=None):

            self.primeiroConteiner = Frame(master)
            self.primeiroConteiner.grid(row=0, column=0, rowspan=2, columnspan=2,
                                        sticky=NW)
            # Listbox Attributes
            self.lista = Listbox(self.primeiroConteiner, width=23, height=8,
                                 font=('MS', '16'), selectmode=BROWSE)
            self.scroll = Scrollbar(self.primeiroConteiner, command=self.lista.yview)
            self.lista.configure(yscrollcommand=self.scroll.set)
            self.lista.pack(side=LEFT)
            self.scroll.pack(side=RIGHT, fill=Y)

            self.fontePadrao = ('Arial', '12', "bold")

            # set width and height from column buttons
            wb_column = 16
            hb_column = 5

            # set width and height from row buttons
            wb_row = 15
            hb_row = 6

            # "UP" Button Attributes
            self.BotaoUp = Button(master, text='UP', font=self.fontePadrao,
                                  width=wb_column, height=hb_column, command=ScrollUp)
            self.BotaoUp.grid(row=0, column=2, sticky=NW)

            # "DOWN" Button Attributes
            self.BotaoDown = Button(master, text='DOWN', font=self.fontePadrao,
                                    width=wb_column, height=hb_column, command=ScrollDown)
            self.BotaoDown.grid(row=1, column=2, sticky=NW)

            # "QUIT" Button Attributes
            self.BotaoQuit = Button(master, text='QUIT', font=self.fontePadrao,
                                    width=wb_column, height=hb_row, command=self.toQuit)
            self.BotaoQuit.grid(row=2, column=2, sticky=SW)

            # "LOAD" Button Attributes
            self.BotaoLoad = Button(master, text='LOAD', font=self.fontePadrao,
                                    width=wb_row, height=hb_row, command=self.fetchData)
            self.BotaoLoad.grid(row=2, column=0, sticky=SW)

            # "BACK" Button Attributes
            self.BotaoBack = Button(master, text='BACK', font=self.fontePadrao,
                                    width=wb_column, height=hb_row, command=backToMain)
            self.BotaoBack.grid(row=2, column=1, sticky=SW)
            
            # Running db reading in screen start
            self.fetchData()

        def fetchData(self):
            """Search name users are in LAB """
            i = 0
            self.lista.delete(0, END)
            # Abrir o arquivo Control.txt em modo leitura
            with open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Control.txt', 'r') as arquivo:
                # laço for para preencher os vetores auxiliares com os nomes
                # E listar os nomes no scroll bar
                for linha in arquivo:
                    nomes = linha.split()
                    vetor_nome.insert(i, nomes[0])
                    vetor_sobrenome.insert(i, nomes[1])
                    vetor_cargo.insert(i, nomes[2])
                    self.lista.insert(END, str(nomes[0] + " " + nomes[1]) + " " + nomes[2])
                    i += 1

            # essa funcao serve para deletar tudo que aparece na scroll bar de modo que
            # ao se apertar o botao LOAD novamente, os dados nao apareçam repetidos
            #self.lista.delete(0, END)
            self.lista.focus_set()

        def toQuit(self):
            # esse metodo retorna uma lista com os items da lista/scroll bar
            items = self.lista.curselection()
            pos = 0

            # laço for para pegar o Indice do item/pessoa que irá sair
            for i in items:
                idx = int(i) - pos
                pos += 1

            now = datetime.now()
            hora = now.strftime("%d/%m/%Y %H:%M:%S")
            with open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Stream.txt', 'a') as arquivo:
                arquivo.writelines(str(vetor_nome[idx]) + " " + str(vetor_sobrenome[idx]) + " " + str(
                    vetor_cargo[idx]) + " " + hora + " Saida" + "\n")

            j = 0
            with open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Control.txt', 'w') as file_control:
                for i in vetor_nome:
                    if i != vetor_nome[idx]:
                        file_control.writelines(
                            str(vetor_nome[j]) + " " + str(vetor_sobrenome[j]) + " " + str(vetor_cargo[j]) + '\n')
                    j += 1

            # método para apagar na lista/scroll bar
            self.lista.delete(idx)

            # falta acrescentar as demais coisas
            gpio.setmode(gpio.BOARD)
            gpio.setup(LOCK_PIN, gpio.OUT)
            gpio.output(LOCK_PIN, gpio.HIGH)
            time.sleep(1)
            gpio.output(LOCK_PIN, gpio.LOW)
            time.sleep(0.5)
            gpio.cleanup()

            # funcao para voltar para a tela01
            time.sleep(1)
            backToMain()

    def ScrollUp():
        keyboard = Controller()
        keyboard.press(Key.up)
        keyboard.release(Key.up)

    def ScrollDown():
        keyboard = Controller()
        keyboard.press(Key.down)
        keyboard.release(Key.down)

    def backToMain():
        root.destroy()
        tela01.telaum()

    # Tkinker Object Instance
    root = Tk()
    ScreenSeven(root)
    root.title("Checkout Screen")
    root.geometry('478x320')
    root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == '__main__':
    telasete()
