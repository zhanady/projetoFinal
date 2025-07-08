import customtkinter as ctk
from banco.GerenciadorFarmacias import GerenciadorFarmacia

class TelaEstoque(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """
        Tela responsável por exibir o estoque de medicamentos.
        Cada medicamento é mostrado em um 'card' com detalhes como:
        nome, quantidade, concentração e princípio ativo.
        """
        super().__init__(master, fg_color="white", **kwargs)

        # Instancia o gerenciador que acessa o banco de dados da farmácia
        self.gerenciador = GerenciadorFarmacia()

        # Scrollable frame que conterá os "cards" dos medicamentos
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            label_text="Estoque de Medicamentos",
            label_font=("Arial", 16, "bold"),
            label_fg_color="white",
            label_text_color="black"
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Busca todos os medicamentos no banco
        estoque = self.gerenciador.buscar_medicamentos()

        # Caso não haja nenhum medicamento, mostra aviso e encerra
        if not estoque:
            ctk.CTkLabel(scroll_frame, text="Nenhum medicamento no estoque.", text_color="red").pack(pady=10)
            return

        # Percorre a lista de medicamentos e exibe cada um em um card
        for i, item in enumerate(estoque):
            # Frame visual para representar um medicamento
            card = ctk.CTkFrame(scroll_frame, fg_color="#F3F4F6", corner_radius=10)
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

            qtd = item.get("quantidade", 0)

            # Se a quantidade for baixa, muda a cor do texto para vermelho
            cor = "red" if qtd < 20 else "black"

            # Nome do medicamento
            ctk.CTkLabel(
                card,
                text=item["medicamento"],
                font=("Arial", 14, "bold"),
                text_color=cor
            ).pack(anchor="w", padx=10, pady=(10, 0))

            # Quantidade disponível
            ctk.CTkLabel(
                card,
                text=f"Quantidade: {qtd}",
                font=("Arial", 12),
                text_color=cor
            ).pack(anchor="w", padx=10)

            # Concentração do medicamento (ex: 500mg)
            ctk.CTkLabel(
                card,
                text=f"Concentração: {item.get('concentracao', '')}",
                font=("Arial", 12),
                text_color="black"
            ).pack(anchor="w", padx=10)

            # Princípio ativo (ex: Dipirona Sódica)
            ctk.CTkLabel(
                card,
                text=f"Princípio ativo: {item.get('principio_ativo', '')}",
                font=("Arial", 12),
                text_color="black"
            ).pack(anchor="w", padx=10, pady=(0, 10))
