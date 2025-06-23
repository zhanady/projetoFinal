import customtkinter as ctk

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, callback_login, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.callback_login = callback_login  # função que será chamada ao logar

        # Área central de login
        container = ctk.CTkFrame(self, fg_color="#F9F9F9", corner_radius=12)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="Login", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        # Campo de usuário
        ctk.CTkLabel(container, text="Usuário", anchor="w").pack(padx=20, anchor="w")
        self.usuario_entry = ctk.CTkEntry(container, width=250)
        self.usuario_entry.pack(padx=20, pady=10)

        # Campo de senha
        ctk.CTkLabel(container, text="Senha", anchor="w").pack(padx=20, anchor="w")
        self.senha_entry = ctk.CTkEntry(container, show="*", width=250)
        self.senha_entry.pack(padx=20, pady=10)

        # Botão de login
        ctk.CTkButton(
            container,
            text="Entrar",
            fg_color="black",
            text_color="white",
            width=250,
            command=self.realizar_login
        ).pack(pady=(10, 20), padx=20)

    def realizar_login(self):
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        # Validação básica (pode ser substituída por autenticação real)
        if usuario and senha:
            self.callback_login(usuario)
        else:
            print("Usuário ou senha vazios")

def app_inicial(usuario):
    print(f"Acessando sistema como: {usuario}")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("500x400")
app.title("Tela de Login")

tela_login = TelaLogin(app, callback_login=app_inicial)
tela_login.pack(fill="both", expand=True)

app.mainloop()
