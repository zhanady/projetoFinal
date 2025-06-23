import customtkinter as ctk

class TelaEstoque(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            label_text="Estoque de Medicamentos",
            label_font=("Arial", 16, "bold"),
            label_fg_color="white",
            label_text_color="black"
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        estoque = [
            {"medicamento": "Dipirona", "concentracao": "500mg", "principio_ativo": "Dipirona Monoidratada", "quantidade": 120},
            {"medicamento": "Paracetamol", "concentracao": "750mg", "principio_ativo": "Paracetamol", "quantidade": 30},
            {"medicamento": "Amoxicilina", "concentracao": "500mg", "principio_ativo": "Amoxicilina Tri-hidratada", "quantidade": 10},
            {"medicamento": "Ibuprofeno", "concentracao": "400mg", "principio_ativo": "Ibuprofeno", "quantidade": 90},
            {"medicamento": "Omeprazol", "concentracao": "20mg", "principio_ativo": "Omeprazol Magnésico", "quantidade": 25},
            {"medicamento": "Azitromicina", "concentracao": "500mg", "principio_ativo": "Azitromicina Dihidratada", "quantidade": 8},
        ]

        for i, item in enumerate(estoque):
            card = ctk.CTkFrame(scroll_frame, fg_color="#F3F4F6", corner_radius=10)
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

            cor = "red" if item["quantidade"] < 20 else "black"

            ctk.CTkLabel(card, text=item["medicamento"], font=("Arial", 14, "bold"), text_color=cor).pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(card, text=f"Quantidade: {item['quantidade']}", font=("Arial", 12), text_color=cor).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Concentração: {item['concentracao']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Princípio ativo: {item['principio_ativo']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10, pady=(0, 10))
