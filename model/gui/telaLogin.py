# tela_login.py
import customtkinter as ctk
from banco.GerenciadorUsuarios import *


class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, callback_login, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.callback_login = callback_login

        container = ctk.CTkFrame(self, fg_color="#F9F9F9", corner_radius=12)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="Login", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        ctk.CTkLabel(container, text="E-mail", anchor="w").pack(padx=20, anchor="w")
        self.usuario_entry = ctk.CTkEntry(container, width=250)
        self.usuario_entry.pack(padx=20, pady=10)

        ctk.CTkLabel(container, text="Senha", anchor="w").pack(padx=20, anchor="w")
        self.senha_entry = ctk.CTkEntry(container, show="*", width=250)
        self.senha_entry.pack(padx=20, pady=10)

        ctk.CTkButton(
            container,
            text="Entrar",
            fg_color="black",
            text_color="white",
            width=250,
            command=self.realizar_login
        ).pack(pady=(10, 20), padx=20)

        self.gerenciador = GerenciadorUsuarios()

    def realizar_login(self):
        email = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not email or not senha:
            print("Usuário ou senha vazios")
            return

        usuario = self.gerenciador.autenticar(email, senha)

        if usuario:
            print(f"Login bem-sucedido. Tipo: {usuario['tipo']}")
            self.callback_login(usuario)  # envia o dicionário com os dados do usuário
        else:
            print("Email ou senha incorretos.")
