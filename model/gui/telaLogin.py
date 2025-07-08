# tela_login.py
import customtkinter as ctk
from banco.GerenciadorUsuarios import *

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, callback_login, **kwargs):
        """
        Tela de login para entrada de e-mail e senha.

        Args:
            master: Janela ou container pai.
            callback_login: Função que será chamada após login bem-sucedido.
            kwargs: Argumentos adicionais passados ao CTkFrame.
        """
        super().__init__(master, fg_color="white", **kwargs)
        self.callback_login = callback_login  # Função para redirecionar após login

        # Container centralizado
        container = ctk.CTkFrame(self, fg_color="#F9F9F9", corner_radius=12)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Título "Login"
        ctk.CTkLabel(container, text="Login", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        # Campo de e-mail
        ctk.CTkLabel(container, text="E-mail", anchor="w").pack(padx=20, anchor="w")
        self.usuario_entry = ctk.CTkEntry(container, width=250)
        self.usuario_entry.pack(padx=20, pady=10)

        # Campo de senha (oculto com *)
        ctk.CTkLabel(container, text="Senha", anchor="w").pack(padx=20, anchor="w")
        self.senha_entry = ctk.CTkEntry(container, show="*", width=250)
        self.senha_entry.pack(padx=20, pady=10)

        # Botão "Entrar"
        ctk.CTkButton(
            container,
            text="Entrar",
            fg_color="black",
            text_color="white",
            width=250,
            command=self.realizar_login  # Ação ao clicar
        ).pack(pady=(10, 20), padx=20)

        # Instancia o gerenciador de usuários (acesso ao banco)
        self.gerenciador = GerenciadorUsuarios()

    def realizar_login(self):
        """
        Lê os campos de e-mail e senha e verifica se são válidos.
        Se o login for correto, chama o callback com os dados do usuário.
        """
        email = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        # Validação simples
        if not email or not senha:
            print("Usuário ou senha vazios")
            return

        # Autenticação com o banco
        usuario = self.gerenciador.autenticar(email, senha)

        if usuario:
            print(f"Login bem-sucedido. Tipo: {usuario['tipo']}")
            self.callback_login(usuario)  # Passa os dados do usuário autenticado
        else:
            print("Email ou senha incorretos.")
