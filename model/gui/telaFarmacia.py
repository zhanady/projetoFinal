import customtkinter as ctk
from gui.telaRelatorios import MenuRelatorios
from gui.telaEstoque import TelaEstoque
from gui.telaChat import ChatScreen

from gui.telaPedido import TelaPedidos  # ← nova importação


class TelaFarmaceutico(ctk.CTkFrame):
    def __init__(self, master, mostrar_chat_callback=None, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)

        self.mostrar_chat_callback = mostrar_chat_callback
        self.menu_relatorio_visivel = False

        self.relatorio_menu = MenuRelatorios(self)
        self.relatorio_menu.place_forget()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#F8F9FA", border_width=1)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="Farmácia", font=("Arial", 16), anchor="w").pack(pady=(20, 10), padx=10, anchor="w")

        ctk.CTkButton(self.sidebar, text="Pedidos", anchor="w", command=self.mostrar_pedidos,
                      fg_color="black", text_color="white", hover_color="#333333").pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Estoque", anchor="w", command=self.mostrar_estoque,
                      fg_color="black", text_color="white", hover_color="#333333").pack(pady=5, padx=10, fill="x")

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

        ctk.CTkButton(self.sidebar, text="Chat", anchor="w",
              fg_color="black", text_color="white", hover_color="#333333",
              command=self.mostrar_chat).pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Log out", anchor="w",
                      fg_color="black", text_color="white", hover_color="#333333").pack(side="bottom", pady=20, padx=10, fill="x")

        # Área principal
        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.mostrar_pedidos()  # tela padrão ao abrir

    def mostrar_chat(self):
        self.trocar_tela(ChatScreen)


    def mostrar_relatorio(self):
        if self.menu_relatorio_visivel:
            self.relatorio_menu.place_forget()
            self.menu_relatorio_visivel = False
        else:
            def place_menu():
                self.update_idletasks()
                x = self.sidebar.winfo_width() + 10
                y = self.btn_relatorios.winfo_rooty() - self.winfo_rooty()
                self.relatorio_menu.place(x=x, y=y)
                self.relatorio_menu.lift()
                self.menu_relatorio_visivel = True

            self.after(10, place_menu)

    def mostrar_estoque(self):
        self.trocar_tela(TelaEstoque)

    def mostrar_pedidos(self):
        self.trocar_tela(TelaPedidos)

    def trocar_tela(self, TelaClasse):
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        nova_tela = TelaClasse(self.area_principal)
        nova_tela.pack(fill="both", expand=True)


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
