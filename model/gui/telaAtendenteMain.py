import customtkinter as ctk
from gui.telaChat import ChatScreen
from gui.telaRelatorios import MenuRelatorios
from banco.GerenciadorPacientes import GerenciadorPacientes

class AppAtendente(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.gerenciador = GerenciadorPacientes()
        self.menu_visivel = False
        self.chat_screen = None
        self.main_frame = None
        self.sidebar = None

        self.criar_sidebar()
        self.criar_tela_cadastro()
        self.criar_menu_relatorio()

        self.usuario_id = None

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="", font=("Arial", 16)).pack(pady=(20, 10))

        ctk.CTkButton(self.sidebar, text="Cadastrar Paciente", anchor="w",
                      fg_color="black", command=self.mostrar_tela_cadastro).pack(pady=10, padx=10, fill="x")

        # ctk.CTkButton(self.sidebar, text="Relatórios", anchor="w",
        #               fg_color="black", command=self.toggle_relatorio_menu).pack(pady=10, padx=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Chat", anchor="w",
                      fg_color="black", command=self.mostrar_tela_chat).pack(pady=10, padx=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Log out", anchor="w",
              fg_color="black", command=self.fechar_app).pack(side="bottom", pady=20, padx=10, fill="x")

    def fechar_app(self):
        self.master.destroy()  # Fecha a janela principal (root)


    def criar_tela_cadastro(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="#F0F0F0")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.main_frame, text="Cadastro de Paciente", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="w")
        ctk.CTkLabel(self.main_frame, text="Preencha os dados do paciente e o encaminhe para triagem").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 20))

        self.entries = []
        labels = ["Name", "CPF", "Telefone", "E-mail", "Data de Nascimento", "Sexo"]
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.main_frame, text=label).grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.main_frame, width=250)
            entry.grid(row=i + 2, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)

        self.entries_right = []
        labels_right = ["Tipo sanguíneo", "Endereco", "Escala Dor",
                        "Escala Glasgow", "Batimentos por Minuto"]
        for i, label in enumerate(labels_right):
            ctk.CTkLabel(self.main_frame, text=label).grid(row=i + 2, column=2, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.main_frame, width=250)
            entry.grid(row=i + 2, column=3, padx=10, pady=5, sticky="w")
            self.entries_right.append(entry)

        ctk.CTkButton(self.main_frame, text="Salvar e encaminhar para triagem",
                      fg_color="black", command=self.salvar_paciente).grid(row=10, column=3, pady=40, sticky="e")
    def mostrar_popup_sucesso(self, mensagem):
        popup = ctk.CTkToplevel(self)
        popup.title("Sucesso")
        popup.geometry("300x120")
        popup.transient(self)  # Garante que fique acima da janela principal
        popup.grab_set()       # Modal

        ctk.CTkLabel(popup, text=mensagem, font=("Arial", 14)).pack(pady=20)

        ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=5)

    def salvar_paciente(self):
        try:
            print(self.entries)
            nome = self.entries[0].get()
            cpf = self.entries[1].get()
            telefone = self.entries[2].get()
            email = self.entries[3].get()
            data_nasc = self.entries[4].get()
            sexo = self.entries[5].get()
            tipo_sang = self.entries_right[0].get()
            endereco = self.entries_right[1].get()
            escala_dor = self.entries_right[2].get()
            escala_glascow = self.entries_right[3].get()
            sinais_vitais = self.entries_right[4].get()
            #status = self.entries_right[2].get()

            print("Nome:", nome)
            print("CPF:", cpf)
            print("Telefone:", telefone)
            print("Email:", email)
            print("Data Nascimento:", data_nasc)
            print("Sexo:", sexo)
            print("Tipo Sanguíneo:", tipo_sang)
            print("Endereço:", endereco)
            #print("Status:", status)


            if not nome or not cpf or not escala_dor or not escala_glascow or not sinais_vitais:
                print("⚠ Nome, CPF, a escala de dor, Glascow e sinais vitais são obrigatórios.")
                return

            id_paciente = self.gerenciador.cadastrar_ou_reativar(
                nome, cpf, telefone, email, data_nasc, sexo,
                tipo_sang, endereco, escala_dor, escala_glascow, sinais_vitais
            )
            print(f"✔ Paciente cadastrado com ID {id_paciente}")
            self.mostrar_popup_sucesso("Paciente cadastrado com sucesso!")

        except Exception as e:
            print(f"Erro ao salvar paciente: {e}")

    def criar_menu_relatorio(self):
        self.relatorio_menu = MenuRelatorios(self)
        self.relatorio_menu.place_forget()

    def toggle_relatorio_menu(self):
        if self.menu_visivel:
            self.relatorio_menu.place_forget()
        else:
            self.relatorio_menu.place(x=210, y=100)
        self.menu_visivel = not self.menu_visivel

    def mostrar_tela_cadastro(self):
        if self.chat_screen:
            self.chat_screen.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def mostrar_tela_chat(self):
        self.main_frame.pack_forget()
        if not self.chat_screen:
            self.chat_screen = ChatScreen(self)
            self.chat_screen.set_usuario_id(self.usuario_id)
        self.chat_screen.pack(fill="both", expand=True)

    def set_usuario_id(self, usuario_id):
        self.usuario_id = usuario_id


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1000x600")
    app = AppAtendente(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
