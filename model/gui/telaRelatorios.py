import customtkinter as ctk

class MenuRelatorios(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=200, corner_radius=5, border_width=1, border_color="#A0A0A0", **kwargs)

        # Opção 1
        ctk.CTkButton(
            self,
            text="Gerar relatório entradas",
            anchor="w",
            text_color="black",
            fg_color="transparent",
            hover_color="#E0E0E0"
        ).pack(fill="x", padx=5, pady=2)

        # Opção 2 (desativada)
        ctk.CTkButton(
            self,
            text="Gerar relatório medicamentos",
            anchor="w",
            text_color="black",
            fg_color="transparent",
            #hover=False,
            hover_color="#E0E0E0"
        ).pack(fill="x", padx=5, pady=2)

        # Opção 3
        ctk.CTkButton(
            self,
            text="Gerar relatório leitos",
            anchor="w",
            text_color="black",
            fg_color="transparent",
            hover_color="#E0E0E0"
        ).pack(fill="x", padx=5, pady=2)

        # Opção 4 (selecionada visualmente)
        ctk.CTkButton(
            self,
            text="Gerar relatório filas",
            anchor="w",
            text_color="black",
            fg_color="transparent",
            hover_color="#E0E0E0"
        ).pack(fill="x", padx=5, pady=2)
