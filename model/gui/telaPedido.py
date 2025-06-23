import customtkinter as ctk

class TelaPedidos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            label_text="Pedidos de Medicamentos",
            label_font=("Arial", 16, "bold"),
            label_fg_color="white",
            label_text_color="black"
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        pedidos = [
            {"medicamento": "Dipirona", "concentracao": "500mg", "principio_ativo": "Dipirona Monoidratada", "urgencia": "alta"},
            {"medicamento": "Paracetamol", "concentracao": "750mg", "principio_ativo": "Paracetamol", "urgencia": "media"},
            {"medicamento": "Amoxicilina", "concentracao": "500mg", "principio_ativo": "Amoxicilina Tri-hidratada", "urgencia": "baixa"},
            {"medicamento": "Ibuprofeno", "concentracao": "400mg", "principio_ativo": "Ibuprofeno", "urgencia": "alta"},
            {"medicamento": "Omeprazol", "concentracao": "20mg", "principio_ativo": "Omeprazol Magnésico", "urgencia": "media"},
            {"medicamento": "Azitromicina", "concentracao": "500mg", "principio_ativo": "Azitromicina Dihidratada", "urgencia": "baixa"},
        ]

        for i, pedido in enumerate(pedidos):
            card = ctk.CTkFrame(scroll_frame, fg_color="#F3F4F6", corner_radius=10)
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

            cor = {
                "alta": "red",
                "media": "orange",
                "baixa": "green"
            }.get(pedido["urgencia"], "gray")

            ctk.CTkLabel(card, text="●", text_color=cor, font=("Arial", 18, "bold")).place(relx=0.95, rely=0.05, anchor="ne")

            ctk.CTkLabel(card, text=pedido["medicamento"], font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(card, text=f"Concentração: {pedido['concentracao']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Princípio ativo: {pedido['principio_ativo']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)

            ctk.CTkButton(card, text="Confirmar",
                          fg_color="black", text_color="white", hover_color="#333333",
                          command=lambda p=pedido: print(f"✔ Pedido confirmado: {p['medicamento']}")).pack(pady=(0, 10), padx=10, anchor="e")
