"""
Title: Biometric Lock User Interface
# Organization: Optima-UFAM
# Screen 2: Search Screen for ADM users
# Description:Starts the Fingerprint search loop only for ROOT ADM users
# Especs: Touchscreen LCD 3,5" 480x320
# Autor: Diego Vieira
# Review: Leonardo Arcanjo
"""
# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# Tkinter Package Execption Handling
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import hashlib
import sqlite3
# Screen
import tela01
import tela03


def teladois():
    class ScreenTwo:  # class
        def __init__(self, master=None):
            # Conteiners Attributes
            self.fontePadrao = ("Arial", "16", "bold")
            self.primeiroContainer = Frame(master)
            self.primeiroContainer["pady"] = 20
            self.primeiroContainer.pack()

            self.segundoContainer = Frame(master)
            self.segundoContainer["padx"] = 20
            self.segundoContainer.pack()

            self.terceiroContainer = Frame(master)
            self.terceiroContainer["padx"] = 10
            self.terceiroContainer.pack()

            self.quartoContainer = Frame(master)
            self.quartoContainer["pady"] = 10
            self.quartoContainer.pack()

            self.quintoContainer = Frame(master)
            self.quintoContainer["pady"] = 5
            self.quintoContainer.pack()

            # Widgets Attributes
            self.titulo = Label(self.primeiroContainer, text="OPTIONS")
            self.titulo["font"] = ("Arial", "18", "bold")
            self.titulo.pack()

            self.nomeLabel = Label(self.segundoContainer, text="Nome", font=self.fontePadrao)
            self.nomeLabel.pack(side=LEFT)

            self.nome = Entry(self.segundoContainer)
            self.nome["width"] = 30
            self.nome["font"] = ["Arial", "16"]
            self.nome.pack(side=LEFT)

            self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
            self.senhaLabel.pack(side=LEFT)

            self.senha = Entry(self.terceiroContainer)
            self.senha["width"] = 30
            self.senha["font"] = ["Arial", "16"]
            self.senha["show"] = "*"
            self.senha.pack(side=LEFT)

            self.autenticar = Button(self.quartoContainer)
            self.autenticar["text"] = "LOGIN"
            self.autenticar["font"] = ("Calibri", "18")
            self.autenticar["width"] = 20
            self.autenticar["height"] = 2
            self.autenticar["command"] = self.verificaSenha
            self.autenticar.pack()

            self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.mensagem.pack()

            self.home = Button(self.quintoContainer)
            self.home["text"] = "MAIN MENU"
            self.home["font"] = ("Calibri", "18")
            self.home["width"] = 20
            self.home["height"] = 2
            self.home["command"] = returntohome
            self.home.pack(side=BOTTOM)

        # Methods
        def verificaSenha(self):
            usuario = self.nome.get()
            senha = self.senha.get()
            puser = usuario.casefold()

            # Verifies if username and user password are in database
            try:
                senha = senha.encode('utf-8')
                senha = hashlib.sha256(senha).hexdigest()

                conn = sqlite3.connect('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db')
                cursor = conn.cursor()

                cursor.execute("""SELECT senhas, admin FROM optima WHERE first_name=?""", (puser,))

                row = cursor.fetchall()

                conn.commit()
                conn.close()

                vetor = []
                i = 0

                for j in row[0]:
                    vetor.insert(i, j)
                    i += 0

                if (vetor[0] == 1) and (vetor[1] == senha):
                    self.mensagem['text'] = "Access Allow"
                    root.destroy()
                    tela03.telatres()
                elif (vetor[0] == 1) and (vetor[1] != senha):
                    self.mensagem['text'] = "Password Wrong"
                else:
                    self.mensagem['text'] = "Access Denied"

            except:
                self.mensagem["text"] = "User does not exist"

    def returntohome():
        """Destroys current screen and calls tela01 module"""
        root.destroy()
        tela01.telaum()

    # Tkinter attributes instance
    root = Tk()
    ScreenTwo(root)
    root.title("Admin Access")
    root.geometry('478x320')
    root.attributes("-fullscreen", True)
    root.mainloop()


if __name__ == "__main__":  # Main
    teladois()
