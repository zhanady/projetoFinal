import customtkinter as ctk

class TelaSolicitarMedicamento(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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

        print(f"📦 Solicitação de medicamento:")
        print(f"→ Nome: {nome}")
        print(f"→ Concentração: {conc}")
        print(f"→ Quantidade: {qtd}")
        print(f"→ Observações: {obs}")

        # Aqui você pode chamar uma função para enviar ao banco, API, etc.
        self.destroy()
