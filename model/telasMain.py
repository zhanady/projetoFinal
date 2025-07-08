import sqlite3

import customtkinter as ctk
from gui.telaLogin import *
from gui.telaMedico import *
from gui.telaAtendenteMain import *
from gui.telaFarmacia import *

app = None  # variável global

def app_inicial(usuario: dict):
    global app
    # Limpa tudo que está na janela
    for widget in app.winfo_children():
        widget.destroy()

    tipo = usuario['tipo']
    if tipo == 0:
        tela_medico = TelaPrincipal(app)
        tela_medico.set_usuario_id(usuario['id'])
        tela_medico.pack(fill="both", expand=True)
    elif tipo == 1:
        tela_atendente = AppAtendente(app)
        tela_atendente.set_usuario_id(usuario['id'])
        tela_atendente.pack(fill="both", expand=True)
    elif tipo == 2:
        tela_farmacia = TelaFarmaceutico(app)
        tela_farmacia.set_usuario_id(usuario['id'])
        tela_farmacia.pack(fill="both", expand=True)
    else:
        print("Tipo de usuário desconhecido")

def main():
    global app
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("500x400")
    app.title("Tela de Login")

    tela_login = TelaLogin(app, callback_login=app_inicial)
    tela_login.pack(fill="both", expand=True)

    app.mainloop()

if __name__ == "__main__":
    main()

#1. login
#verificar se o usuario é atendente, medico ou farmaceutico
#se for farmaceutico -> ir para telaFarmacio
#se for medico -> telaMedico
#se for atendente -> tela atendente main