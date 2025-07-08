import customtkinter as ctk
from banco.GerenciadorPedidosFarmacia import GerenciadorPedidosFarmacia


class TelaSolicitarMedicamento(ctk.CTkToplevel):
    def __init__(self, master, atualizar_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.gerenciador = GerenciadorPedidosFarmacia()
        self.atualizar_callback = atualizar_callback
        self.profissional_id = None
        self.paciente_id = None

        self.title("Solicitar Medicamento")
        self.geometry("400x400")
        self.configure(fg_color="white")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Solicitação de Medicamento", font=("Arial", 16, "bold")).pack(pady=20)

        # Campos de entrada
        self.nome = ctk.CTkEntry(self, placeholder_text="Nome do Medicamento")
        self.nome.pack(pady=10, padx=20, fill="x")

        self.concentracao = ctk.CTkEntry(self, placeholder_text="Concentração (ex: 500mg)")
        self.concentracao.pack(pady=10, padx=20, fill="x")

        self.quantidade = ctk.CTkEntry(self, placeholder_text="Quantidade")
        self.quantidade.pack(pady=10, padx=20, fill="x")

        self.obs = ctk.CTkTextbox(self, height=80)
        self.obs.pack(pady=10, padx=20, fill="x")
        self.obs.insert("1.0", "Observações adicionais...")

        # Botão de confirmar
        ctk.CTkButton(self, text="Confirmar Solicitação", fg_color="green", command=self.confirmar).pack(pady=20)

    def confirmar(self):
        nome = self.nome.get()
        conc = self.concentracao.get()
        qtd = self.quantidade.get()
        obs = self.obs.get("1.0", "end").strip()

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
                "principio_ativo": nome,  # ou você pode deixar um campo separado depois
                "concentracao": conc,
                "quantidade_solicitada": int(qtd),
                "urgencia": "media"  # ou você pode tornar isso um campo selecionável
            }

            self.gerenciador.registrar_pedido(dados)
            print("✔ Pedido registrado com sucesso.")

            if self.atualizar_callback:
                self.atualizar_callback()  # atualiza a lista na TelaPedidos

            self.destroy()

        except Exception as e:
            print(f"Erro ao registrar pedido: {e}")

    def set_profissional_paciente_id(self, profissional_id, paciente_id):
        self.profissional_id = profissional_id
        self.paciente_id = paciente_id
