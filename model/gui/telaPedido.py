import customtkinter as ctk
from banco.GerenciadorPedidosFarmacia import GerenciadorPedidosFarmacia  # Gerenciador que lida com os dados dos pedidos

# Classe que representa a interface onde os pedidos de medicamentos são exibidos e confirmados
class TelaPedidos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Inicializa o frame principal da tela de pedidos
        super().__init__(master, fg_color="white", **kwargs)
        self.gerenciador = GerenciadorPedidosFarmacia()  # Responsável por buscar e atualizar pedidos

        # Dicionário que armazena os widgets (cards) dos pedidos para acesso posterior
        self.cards_widgets = {}  # chave = id do pedido, valor = widget (card)

        # Frame com rolagem que exibirá os pedidos pendentes em forma de cartões
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            label_text="Pedidos de Medicamentos",
            label_font=("Arial", 16, "bold"),
            label_fg_color="white",
            label_text_color="black"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Chama função que monta a lista de pedidos visuais
        self.atualizar_lista_pedidos()

    def mostrar_popup_sucesso(self, mensagem):
        # Cria uma janela popup para mostrar mensagem de sucesso ao confirmar um pedido
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmação")
        popup.geometry("300x120")
        popup.transient(self)  # Mantém o popup sobre a janela principal
        popup.grab_set()       # Bloqueia interações fora do popup enquanto ele está ativo

        ctk.CTkLabel(popup, text=mensagem, font=("Arial", 14)).pack(pady=20)
        ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=5)

    def atualizar_lista_pedidos(self):
        # Atualiza a lista de pedidos exibidos, removendo os antigos e criando novos

        # Remove todos os widgets existentes no scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Busca os pedidos pendentes no banco
        pedidos = self.gerenciador.buscar_pedidos_pendentes()

        # Cria um "card" visual para cada pedido
        for i, pedido in enumerate(pedidos):
            card = ctk.CTkFrame(self.scroll_frame, fg_color="#F3F4F6", corner_radius=10)
            self.cards_widgets[pedido["id"]] = card  # Guarda o card no dicionário

            # Posiciona os cards em grade (2 por linha)
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

            # Define cor da bolinha com base na urgência
            urgencia = pedido.get("urgencia", "baixa")
            cor = {
                "alta": "red",
                "media": "orange",
                "baixa": "green"
            }.get(urgencia, "gray")

            # Bolinha de cor da urgência no canto superior direito
            ctk.CTkLabel(card, text="●", text_color=cor, font=("Arial", 18, "bold")).place(relx=0.95, rely=0.05, anchor="ne")

            # Informações do pedido
            ctk.CTkLabel(card, text=pedido["medicamento"], font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(card, text=f"Concentração: {pedido['concentracao']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Princípio ativo: {pedido['principio_ativo']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Quantidade solicitada: {pedido['quantidade_solicitada']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)

            # Botão para confirmar o pedido (chama função com ID e dados do pedido)
            ctk.CTkButton(
                card,
                text="Confirmar",
                fg_color="black",
                text_color="white",
                hover_color="#333333",
                command=lambda p=pedido: self.confirmar_pedido(p["id"], p["medicamento"], p["quantidade_solicitada"])
            ).pack(pady=(0, 10), padx=10, anchor="e")

    def confirmar_pedido(self, pedido_id, medicamento_nome, quantidade):
        # Tenta confirmar o pedido no banco e atualiza visualmente
        sucesso = self.gerenciador.confirmar_pedido(pedido_id, medicamento_nome, quantidade)
        if sucesso:
            print(f"✔ Pedido {pedido_id} confirmado.")

            # Mostra uma janela de confirmação visual
            self.mostrar_popup_sucesso("Pedido confirmado com sucesso!")

            # Remove visualmente o card do pedido
            card = self.cards_widgets.pop(pedido_id, None)
            if card:
                card.destroy()

        else:
            print(f"Erro ao confirmar pedido {pedido_id}. Verifique estoque ou dados.")
