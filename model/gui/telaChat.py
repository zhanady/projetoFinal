import customtkinter as ctk
from PIL import Image
import os

class ChatScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,  **kwargs)

        # Cores
        black = "#000000"
        gray_hover = "#E0E0E0"
        msg_bg = "#CCCCCC"
        msg_sent_bg = "#FFFFFF"
        border_gray = "#B0B0B0"

        # Frame lateral - Contatos com contorno
        self.sidebar_middle = ctk.CTkFrame(self, width=200, border_width=1, border_color=border_gray)
        self.sidebar_middle.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar_middle, text="Chat", font=("Arial", 16), text_color=black).pack(pady=(20, 10))

        # Contato 1
        ctk.CTkButton(self.sidebar_middle, text="Avisos", anchor="w", fg_color=black, hover_color=gray_hover).pack(pady=0, padx=10, fill="x")
        ctk.CTkFrame(self.sidebar_middle, height=1, fg_color=border_gray).pack(fill="x", padx=10)

        # Contato 2
        ctk.CTkButton(self.sidebar_middle, text="Fulano", anchor="w", fg_color=black, hover_color=gray_hover).pack(pady=0, padx=10, fill="x")
        ctk.CTkFrame(self.sidebar_middle, height=1, fg_color=border_gray).pack(fill="x", padx=10)

        # Área principal da conversa
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(side="left", fill="both", expand=True)

        # Topo da conversa com contorno no nome
        top_bar = ctk.CTkFrame(self.chat_frame, height=40, fg_color="#D3D3D3", border_width=1, border_color=border_gray)
        top_bar.pack(fill="x")

        ctk.CTkLabel(top_bar, text="Fulano", text_color=black, anchor="w", justify="left").pack(padx=6, pady=2, fill="x")

        # Área de mensagens
        # Área de mensagens com scroll
        self.messages_area = ctk.CTkScrollableFrame(self.chat_frame)
        self.messages_area.pack(fill="both", expand=True, padx=15, pady=10)


        # Exemplo de mensagens iniciais
        msg_frame_left = ctk.CTkFrame(self.messages_area, fg_color="transparent")
        msg_frame_left.pack(anchor="w", pady=5, padx=10, fill="x")
        ctk.CTkLabel(msg_frame_left, text="Mensagem recebida", width=300, height=30,
                     fg_color=msg_bg, corner_radius=6).pack(anchor="w")

        msg_frame_right = ctk.CTkFrame(self.messages_area, fg_color="transparent")
        msg_frame_right.pack(anchor="e", pady=5, padx=10, fill="x")
        ctk.CTkLabel(msg_frame_right, text="Mensagem enviada", width=300, height=30,
                     fg_color=msg_sent_bg, corner_radius=6, text_color=black).pack(anchor="e")

        # Barra inferior de digitação
        bottom_bar = ctk.CTkFrame(self.chat_frame, height=90, fg_color="#E0E0E0")
        bottom_bar.pack(fill="x", side="bottom")

        self.entry = ctk.CTkEntry(bottom_bar, width=550, height=30)
        self.entry.pack(side="left", padx=(10, 5), pady=5)

        icon_path = os.path.join(os.path.dirname(__file__), "icons", "arrow-right-circle.png")
        arrow_icon = ctk.CTkImage(Image.open(icon_path), size=(28, 28))

        self.send_button = ctk.CTkButton(
            bottom_bar,
            text="",
            image=arrow_icon,
            width=40,
            height=32,
            fg_color="transparent",
            hover_color="#D0D0D0",
            command=self.enviar_mensagem
        )
        self.send_button.pack(side="left", padx=5, pady=5)

        # Enviar com ENTER
        self.entry.bind("<Return>", lambda event: self.enviar_mensagem())

    def enviar_mensagem(self):
        mensagem = self.entry.get().strip()
        self.messages_area._parent_canvas.yview_moveto(1.0)  # rola para o final


        if mensagem == "":
            return  # Ignora mensagens vazias

        # Cria frame para a mensagem enviada (à direita)
        msg_frame = ctk.CTkFrame(self.messages_area, fg_color="transparent")
        msg_frame.pack(anchor="e", pady=5, padx=10, fill="x")

        ctk.CTkLabel(
            msg_frame,
            text=mensagem,
            width=300,
            height=30,
            fg_color="#FFFFFF",
            text_color="#000000",
            corner_radius=6,
            anchor="e"
        ).pack(anchor="e")

        self.entry.delete(0, "end")  # Limpa o campo

# Execução
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Chat App")

    chat_screen = ChatScreen(app)
    chat_screen.pack(fill="both", expand=True)

    app.mainloop()
