import customtkinter as ctk
from banco.GerenciadorPedidosFarmacia import GerenciadorPedidosFarmacia  # ajuste o caminho conforme seu projeto

class TelaPedidos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.gerenciador = GerenciadorPedidosFarmacia()

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            label_text="Pedidos de Medicamentos",
            label_font=("Arial", 16, "bold"),
            label_fg_color="white",
            label_text_color="black"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.atualizar_lista_pedidos()

    def atualizar_lista_pedidos(self):
        # Limpar antigos widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        pedidos = self.gerenciador.buscar_pedidos_pendentes()

        for i, pedido in enumerate(pedidos):
            card = ctk.CTkFrame(self.scroll_frame, fg_color="#F3F4F6", corner_radius=10)
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

            urgencia = pedido.get("urgencia", "baixa")
            cor = {
                "alta": "red",
                "media": "orange",
                "baixa": "green"
            }.get(urgencia, "gray")

            ctk.CTkLabel(card, text="●", text_color=cor, font=("Arial", 18, "bold")).place(relx=0.95, rely=0.05, anchor="ne")
            ctk.CTkLabel(card, text=pedido["medicamento"], font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(card, text=f"Concentração: {pedido['concentracao']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Princípio ativo: {pedido['principio_ativo']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Quantidade solicitada: {pedido['quantidade_solicitada']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)

            ctk.CTkButton(card, text="Confirmar",
                          fg_color="black", text_color="white", hover_color="#333333",
                          command=lambda p=pedido: self.confirmar_pedido(p["id"], p["medicamento"], p["quantidade_solicitada"])
                          ).pack(pady=(0, 10), padx=10, anchor="e")

    def confirmar_pedido(self, pedido_id, medicamento_nome, quantidade):
        sucesso = self.gerenciador.confirmar_pedido(pedido_id, medicamento_nome, quantidade)
        if sucesso:
            print(f"✔ Pedido {pedido_id} confirmado.")
            self.atualizar_lista_pedidos()
        else:
            print(f"Erro ao confirmar pedido {pedido_id}. Verifique estoque ou dados.")
