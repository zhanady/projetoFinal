import customtkinter as ctk
from banco.GerenciadorPedidosFarmacia import GerenciadorPedidosFarmacia


class TelaSolicitarMedicamento(ctk.CTkToplevel):
    def __init__(self, master, atualizar_callback=None, **kwargs):
        # Inicializa a janela Toplevel (secundária) herdada de CTkToplevel
        super().__init__(master, **kwargs)
        self.gerenciador = GerenciadorPedidosFarmacia()
        self.atualizar_callback = atualizar_callback
        self.profissional_id = None
        self.paciente_id = None

        # Configurações da janela
        self.title("Solicitar Medicamento")
        self.geometry("400x400")
        self.configure(fg_color="white")
        self.resizable(False, False)

        # Título principal da janela
        ctk.CTkLabel(self, text="Solicitação de Medicamento", font=("Arial", 16, "bold")).pack(pady=20)

        # Campo de entrada: Nome do Medicamento (obrigatório)
        self.nome = ctk.CTkEntry(self, placeholder_text="Nome do Medicamento")
        self.nome.pack(pady=10, padx=20, fill="x")

        # Campo de entrada: Concentração do Medicamento (ex: "500mg") (obrigatório)
        self.concentracao = ctk.CTkEntry(self, placeholder_text="Concentração (ex: 500mg)")
        self.concentracao.pack(pady=10, padx=20, fill="x")

        # Campo de entrada: Quantidade solicitada (obrigatório)
        self.quantidade = ctk.CTkEntry(self, placeholder_text="Quantidade")
        self.quantidade.pack(pady=10, padx=20, fill="x")

        # Campo de texto multilinha: Observações adicionais (opcional)
        self.obs = ctk.CTkTextbox(self, height=80)
        self.obs.pack(pady=10, padx=20, fill="x")
        self.obs.insert("1.0", "Observações adicionais...")

        # Botão que confirma e registra a solicitação
        ctk.CTkButton(self, text="Confirmar Solicitação", fg_color="green", command=self.confirmar).pack(pady=20)

    def confirmar(self):
        # Coleta os dados inseridos nos campos
        nome = self.nome.get()
        conc = self.concentracao.get()
        qtd = self.quantidade.get()
        obs = self.obs.get("1.0", "end").strip()

        # Verifica se os campos obrigatórios foram preenchidos
        if not nome or not conc or not qtd:
            print("❗ Preencha todos os campos obrigatórios.")
            return

        try:
            if self.profissional_id is None or self.paciente_id is None:
                raise Exception("É necessário existir um profissional e um paciente configurado")

            dados = {
                "paciente_id": self.paciente_id,
                "profissional_id": self.profissional_id,
                "medicamento": nome,
                "principio_ativo": nome,  # Por enquanto, assume o mesmo nome do medicamento
                "concentracao": conc,
                "quantidade_solicitada": int(qtd),
                "urgencia": "media"  # Valor fixo; pode futuramente virar um campo selecionável
            }

            # Registra o pedido no sistema por meio do gerenciador
            self.gerenciador.registrar_pedido(dados)
            print("✔ Pedido registrado com sucesso.")

            # Se houver callback definido, chama-o para atualizar a tela anterior
            if self.atualizar_callback:
                self.atualizar_callback()

            # Fecha a janela após o sucesso do registro
            self.destroy()

        except Exception as e:
            # Em caso de erro durante o registro, exibe o erro no terminal
            print(f"Erro ao registrar pedido: {e}")

    def set_profissional_paciente_id(self, profissional_id, paciente_id):
        self.profissional_id = profissional_id
        self.paciente_id = paciente_id
