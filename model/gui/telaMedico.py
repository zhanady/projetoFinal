import customtkinter as ctk
from gui.telaFila import TelaFila
from gui.telaChat import ChatScreen
from gui.telaRelatorios import MenuRelatorios
from gui.telaSolicitarRemedios import TelaSolicitarMedicamento
from gui.telaLeitos import TelaLeitos


class TelaMedico(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.relatorio_menu = MenuRelatorios(self)
        self.relatorio_menu.place_forget()
        self.menu_relatorio_visivel = False
        self.paciente = paciente
        self.chat_screen = None

        
        # Área principal
        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.mostrar_atendimento()

    def limpar_area_principal(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        self.chat_screen = None

    def mostrar_fila(self):
        self.limpar_area_principal()
        tela_fila = TelaFila(self.area_principal, abrir_atendimento_callback=self.mostrar_atendimento)
        tela_fila.pack(fill="both", expand=True)
    
    def mostrar_leitos(self):
        self.limpar_area_principal()
        tela_leitos = TelaLeitos(self.area_principal)
        tela_leitos.pack(fill="both", expand=True)



    def mostrar_atendimento(self):
        self.limpar_area_principal()

        content_frame = ctk.CTkFrame(self.area_principal, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = ctk.CTkFrame(content_frame, fg_color="#FAFAFA", corner_radius=8)
        top_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Dados
        dados_frame = ctk.CTkFrame(top_frame, fg_color="white")
        dados_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        ctk.CTkLabel(dados_frame, text="Dados", font=("Arial", 14, "bold")).pack(anchor="w")
        campos = [
            ("Nome", "nome"),
            ("Data de nascimento", "data_nascimento"),
            ("Sexo", "sexo"),
            ("Status", "status")
        ]

        for label, chave in campos:
            ctk.CTkLabel(dados_frame, text=label, anchor="w", justify="left").pack(fill="x", padx=5, pady=(5, 0))
            entry = ctk.CTkEntry(dados_frame, width=200)
            entry.insert(0, self.paciente.get(chave, ""))
            entry.pack(anchor="w", padx=5)


        # Sintomas
        sintomas_frame = ctk.CTkFrame(top_frame, fg_color="white")
        sintomas_frame.pack(side="left", fill="both", expand=True, padx=(5, 5), pady=10)

        ctk.CTkLabel(sintomas_frame, text="Sintomas", font=("Arial", 14, "bold")).pack(anchor="w", padx=5)
        self.sintomas_vars = {}
        for sintoma in ["Febre", "Tosse", "Dor de garganta"]:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(sintomas_frame, text=sintoma, variable=var).pack(anchor="w", padx=5)
            self.sintomas_vars[sintoma] = var

        ctk.CTkLabel(sintomas_frame, text="Descrição").pack(anchor="w", padx=5, pady=(5, 0))
        ctk.CTkEntry(sintomas_frame, width=200).pack(anchor="w", padx=5)

        # Histórico
        historico_frame = ctk.CTkFrame(top_frame, fg_color="white", border_width=1, corner_radius=8)
        historico_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        ctk.CTkLabel(historico_frame, text="Histórico do Paciente", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        historico_textos = [
            "12/06/2025 - Consulta: Dor de cabeça e febre",
            "01/06/2025 - Retorno: Quadro estável",
            "20/05/2025 - Triagem inicial: Pressão alta"
        ]

        for item in historico_textos:
            ctk.CTkLabel(historico_frame, text=f"• {item}", anchor="w", justify="left").pack(anchor="w", padx=10, pady=2)

        # Diagnóstico
        diagnostico_frame = ctk.CTkFrame(content_frame, fg_color="#FAFAFA", corner_radius=8)
        diagnostico_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(diagnostico_frame, text="Possível diagnóstico", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkLabel(diagnostico_frame, text="Descrição").pack(anchor="w", padx=10, pady=(5, 0))
        ctk.CTkEntry(diagnostico_frame, width=300).pack(anchor="w", padx=10)

        # Botões
        botoes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(botoes_frame, text="Salvar", fg_color="black", text_color="white").pack(side="right", padx=5)
        ctk.CTkButton(botoes_frame, text="Internar", fg_color="black", text_color="white").pack(side="right", padx=5)
        ctk.CTkButton(botoes_frame, text="Dar alta", fg_color="black", text_color="white").pack(side="right", padx=5)
        ctk.CTkButton(botoes_frame, text="Solicitar remédios", fg_color="black", text_color="white", command=self.abrir_solicitacao_medicamento).pack(side="right", padx=5)
        ctk.CTkButton(botoes_frame, text="Chamar para atendimento", fg_color="black", text_color="white").pack(side="right", padx=5)


    def mostrar_chat(self):
        self.limpar_area_principal()
        self.chat_screen = ChatScreen(self.area_principal)
        self.chat_screen.pack(fill="both", expand=True)
    
    def abrir_solicitacao_medicamento(self):
        TelaSolicitarMedicamento(self)



    def mostrar_relatorio(self, event):
        if self.menu_relatorio_visivel:
            self.relatorio_menu.place_forget()
            self.menu_relatorio_visivel = False
        else:
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            self.relatorio_menu.place(x=x + 10, y=y + 10)
            self.menu_relatorio_visivel = True


class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.menu_relatorio_visivel = False

        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#F8F9FA", border_width=1)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="My Account", font=("Arial", 16)).pack(pady=(20, 10))

        ctk.CTkButton(self.sidebar, text="Fila", fg_color="black", anchor="w", command=self.mostrar_fila).pack(padx=10, pady=5, fill="x")
        #ctk.CTkButton(self.sidebar, text="Atendimento", fg_color="black", anchor="w", command=self.mostrar_atendimento).pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Chat", fg_color="black", anchor="w", command=self.mostrar_chat).pack(padx=10, pady=5, fill="x")
        self.btn_leitos = ctk.CTkButton(self.sidebar, anchor="w", text="Leitos", fg_color="black", command=self.mostrar_leitos )
        self.btn_leitos.pack(padx=10, pady=5, fill="x")

        btn_relatorios = ctk.CTkButton(self.sidebar, text="Relatórios", fg_color="black", anchor="w")
        btn_relatorios.pack(padx=10, pady=5, fill="x")
        btn_relatorios.bind("<Button-1>", self.mostrar_relatorio)

        ctk.CTkButton(self.sidebar, text="Logout", fg_color="black", anchor="w", command=self.quit).pack(side="bottom", padx=10, pady=20, fill="x")

        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.menu_relatorio = MenuRelatorios(self)
        self.menu_relatorio.place_forget()

        self.mostrar_fila()

    def limpar_area_principal(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def mostrar_fila(self):
        self.limpar_area_principal()
        tela = TelaFila(self.area_principal, abrir_atendimento_callback=self.mostrar_atendimento)
        tela.pack(fill="both", expand=True)
    
    def mostrar_leitos(self):
        self.limpar_area_principal()

        def abrir_atendimento():
            self.mostrar_atendimento()

        tela = TelaLeitos(self.area_principal, abrir_atendimento_callback=abrir_atendimento)
        tela.pack(fill="both", expand=True)



    def mostrar_atendimento(self, paciente):
        self.limpar_area_principal()
        tela = TelaMedico(self.area_principal, paciente=paciente)
        tela.pack(fill="both", expand=True)

    def mostrar_chat(self):
        self.limpar_area_principal()
        tela = ChatScreen(self.area_principal)
        tela.pack(fill="both", expand=True)

    def mostrar_relatorio(self, event):
        if self.menu_relatorio_visivel:
            self.menu_relatorio.place_forget()
            self.menu_relatorio_visivel = False
        else:
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            self.menu_relatorio.place(x=x + 10, y=y + 10)
            self.menu_relatorio_visivel = True


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Sistema Hospitalar")
    app.geometry("1200x700")

    tela = TelaPrincipal(app)
    tela.pack(fill="both", expand=True)

    app.mainloop()
