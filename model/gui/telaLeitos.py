import customtkinter as ctk
from PIL import Image, ImageTk
import os


class TelaLeitos(ctk.CTkFrame):
    def __init__(self, master, abrir_atendimento_callback=None, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.abrir_atendimento_callback = abrir_atendimento_callback

        # Caminhos seguros para as imagens
        base_path = os.path.dirname(__file__)
        self.caminho_cama = os.path.join(base_path, "icons", "bed-single.png")
        self.caminho_paciente = os.path.join(base_path, "icons", "user.png")

        # Carregar imagens redimensionadas
        self.tk_cama = ImageTk.PhotoImage(Image.open(self.caminho_cama).resize((120, 120)))
        self.tk_paciente = None
        if os.path.exists(self.caminho_paciente):
            self.tk_paciente = ImageTk.PhotoImage(Image.open(self.caminho_paciente).resize((30, 30)))

        # Estado dos leitos
        self.leitos = [
            {"ocupado": True, "nome": "João Silva"},
            {"ocupado": True, "nome": "Maria Costa"},
            {"ocupado": False, "nome": ""},
            {"ocupado": False, "nome": ""},
            {"ocupado": False, "nome": ""},
            {"ocupado": False, "nome": ""},
            {"ocupado": False, "nome": ""},
            {"ocupado": False, "nome": ""},
        ]

        self.criar_grid_leitos()

    def criar_grid_leitos(self):
        container = ctk.CTkFrame(self, fg_color="white")
        container.pack(expand=True)

        linhas, colunas = 2, 4
        for i in range(linhas):
            for j in range(colunas):
                idx = i * colunas + j
                if idx >= len(self.leitos):
                    continue

                leito = self.leitos[idx]
                frame_leito = ctk.CTkFrame(container, width=160, height=190, fg_color="white", corner_radius=10)
                frame_leito.grid(row=i, column=j, padx=30, pady=30)
                frame_leito.grid_propagate(False)

                # Canvas da cama
                canvas = ctk.CTkCanvas(frame_leito, width=120, height=120, bg="white", highlightthickness=0)
                canvas.pack()

                # Mostra cama
                canvas.create_image(60, 60, image=self.tk_cama)

                # Mostra personagem em cima da cama se estiver ocupado
                if leito["ocupado"] and self.tk_paciente:
                    canvas.create_image(60, 35, image=self.tk_paciente)

                # Clique no leito
                canvas.bind("<Button-1>", lambda e, i=idx: self.on_leito_click(i))

                # Nome do paciente
                nome_label = ctk.CTkLabel(
                    frame_leito,
                    text=leito["nome"] if leito["ocupado"] else "",
                    font=("Arial", 12),
                    text_color="black"
                )
                nome_label.pack(pady=5)

    def on_leito_click(self, idx):
        print(f"Leito {idx + 1} clicado")
        if self.abrir_atendimento_callback:
            self.abrir_atendimento_callback()
