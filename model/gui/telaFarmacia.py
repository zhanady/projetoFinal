import customtkinter as ctk
from gui.telaRelatorios import MenuRelatorios
from gui.telaEstoque import TelaEstoque
from gui.telaChat import ChatScreen
from gui.telaPedido import TelaPedidos  # ← nova importação

# Classe principal da interface para o farmacêutico
class TelaFarmaceutico(ctk.CTkFrame):
    def __init__(self, master, mostrar_chat_callback=None, **kwargs):
        """
        Tela principal para o farmacêutico, com navegação para:
        - Pedidos
        - Estoque
        - Relatórios
        - Chat
        """
        super().__init__(master, fg_color="white", **kwargs)

        self.mostrar_chat_callback = mostrar_chat_callback  # Callback externo (opcional)
        self.menu_relatorio_visivel = False  # Estado do menu de relatório

        self.relatorio_menu = MenuRelatorios(self)  # Instancia o menu de relatórios flutuante

        # Sidebar (menu lateral esquerdo)
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#F8F9FA", border_width=1)
        self.sidebar.pack(side="left", fill="y")

        # Título
        ctk.CTkLabel(self.sidebar, text="Farmácia", font=("Arial", 16), anchor="w").pack(pady=(20, 10), padx=10, anchor="w")

        # Botão de Pedidos
        ctk.CTkButton(self.sidebar, text="Pedidos", anchor="w", command=self.mostrar_pedidos,
                      fg_color="black", text_color="white", hover_color="#333333").pack(pady=5, padx=10, fill="x")

        # Botão de Estoque
        ctk.CTkButton(self.sidebar, text="Estoque", anchor="w", command=self.mostrar_estoque,
                      fg_color="black", text_color="white", hover_color="#333333").pack(pady=5, padx=10, fill="x")

        # Botão de Relatórios
        self.btn_relatorios = ctk.CTkButton(
            self.sidebar,
            text="Relatórios",
            fg_color="black",
            anchor="w",
            text_color="white",
            hover_color="#333333",
            command=self.mostrar_relatorio
        )
        self.btn_relatorios.pack(padx=10, pady=5, fill="x")

        # Botão de Chat
        ctk.CTkButton(self.sidebar, text="Chat", anchor="w",
              fg_color="black", text_color="white", hover_color="#333333",
              command=self.mostrar_chat).pack(pady=5, padx=10, fill="x")

        # Botão de logout
        ctk.CTkButton(self.sidebar, text="Log out", anchor="w",
              fg_color="black", command=self.fechar_app).pack(side="bottom", pady=20, padx=10, fill="x")

        # Área principal da tela (onde as telas dinâmicas são exibidas)
        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.mostrar_pedidos()  # Exibe a tela de pedidos ao iniciar

    def mostrar_chat(self):
        """Alterna para a tela de chat."""
        self.trocar_tela(ChatScreen)

    def mostrar_relatorio(self):
        """Exibe ou oculta o menu flutuante de relatórios."""
        if self.menu_relatorio_visivel:
            self.relatorio_menu.place_forget()
            self.menu_relatorio_visivel = False
        else:
            def place_menu():
                self.update_idletasks()  # Garante atualização de layout
                x = self.sidebar.winfo_width() + 10
                y = self.btn_relatorios.winfo_rooty() - self.winfo_rooty()
                self.relatorio_menu.place(x=x, y=y)
                self.relatorio_menu.lift()
                self.menu_relatorio_visivel = True

            self.after(10, place_menu)

    def mostrar_estoque(self):
        """Alterna para a tela de estoque de medicamentos."""
        self.trocar_tela(TelaEstoque)

    def fechar_app(self):
        """Fecha completamente a aplicação."""
        self.master.destroy()

    def mostrar_pedidos(self):
        """Alterna para a tela de pedidos da farmácia."""
        self.trocar_tela(TelaPedidos)

    def trocar_tela(self, TelaClasse):
        """
        Remove widgets anteriores da área principal e carrega a nova tela.
        Args:
            TelaClasse: classe da tela a ser instanciada (ex: TelaEstoque)
        """
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        nova_tela = TelaClasse(self.area_principal)
        nova_tela.pack(fill="both", expand=True)

# Execução isolada para testes
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = ctk.CTk()
    app.geometry("1200x700")
    app.title("Farmacêutico")

    def dummy_chat():
        print("🗨 Chat aberto")

    tela = TelaFarmaceutico(app, mostrar_chat_callback=dummy_chat)
    tela.pack(fill="both", expand=True)

    app.mainloop()
