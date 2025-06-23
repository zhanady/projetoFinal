import os
import customtkinter as ctk
from PIL import Image


class TelaFila(ctk.CTkFrame):
    def __init__(self, master, abrir_atendimento_callback, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.abrir_atendimento_callback = abrir_atendimento_callback

        # Caminho do ícone
        icone_path = os.path.join(os.path.dirname(__file__), "icons", "user.png")

        # Carregar a imagem
        self.icone_paciente = ctk.CTkImage(
            light_image=Image.open(icone_path),
            dark_image=Image.open(icone_path),
            size=(40, 40)
        )

        # ====== Fila de Triagem ======
        titulo_triagem = ctk.CTkLabel(self, text="Fila triagem", font=ctk.CTkFont(size=18, weight="bold"))
        titulo_triagem.pack(anchor="w", pady=(20, 5), padx=20)

        subtitulo_triagem = ctk.CTkLabel(self, text="Clique para mais detalhes", text_color="blue")
        subtitulo_triagem.pack(anchor="w", padx=20)

        frame_triagem = ctk.CTkFrame(self, fg_color="#F8F9FA")
        frame_triagem.pack(anchor="w", padx=20, pady=10)

        pacientes_triagem = ["Fulano", "Fulaninho"]
        for paciente in pacientes_triagem:
            self.criar_card_paciente(frame_triagem, paciente)

        # ====== Fila de Atendimento Médico ======
        titulo_atendimento = ctk.CTkLabel(self, text="Fila atendimento médico", font=ctk.CTkFont(size=18, weight="bold"))
        titulo_atendimento.pack(anchor="w", pady=(30, 5), padx=20)

        subtitulo_atendimento = ctk.CTkLabel(self, text="Clique para mais detalhes", text_color="blue")
        subtitulo_atendimento.pack(anchor="w", padx=20)

        frame_atendimento = ctk.CTkFrame(self, fg_color="#F8F9FA")
        frame_atendimento.pack(anchor="w", padx=20, pady=10)

        pacientes_atendimento = ["Fulano", "Fulaninho"]
        for paciente in pacientes_atendimento:
            self.criar_card_paciente(frame_atendimento, paciente)

    def criar_card_paciente(self, parent, paciente):
        frame = ctk.CTkFrame(parent, fg_color="white")
        frame.pack(side="left", padx=20, pady=10)

        # Imagem do paciente
        label_img = ctk.CTkLabel(frame, image=self.icone_paciente, text="")
        label_img.pack(pady=(5, 2))

        # Nome do paciente (clicável)
        label_nome = ctk.CTkLabel(
            frame,
            text=paciente,
            font=ctk.CTkFont(size=14),
            cursor="hand2"
        )
        label_nome.pack()
        label_nome.bind("<Button-1>", lambda e, p=paciente: self.abrir_paciente(p))

    def abrir_paciente(self, paciente):
        print(f"Abrindo dados do paciente: {paciente}")
        self.abrir_atendimento_callback()
