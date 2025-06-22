import customtkinter as ctk
from telaChat import ChatScreen
from telaRelatorios import MenuRelatorios

# Configuração inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color="white")
app.geometry("1000x600")
app.title("Atendente")

main_frame = None
chat_screen = None

# Estado do menu de relatórios
menu_visivel = False
relatorio_menu = MenuRelatorios(app)
relatorio_menu.place_forget()  

def toggle_relatorio_menu():
    global menu_visivel
    if menu_visivel:
        relatorio_menu.place_forget()
    else:
        relatorio_menu.place(x=210, y=100)  # ajuste a posição conforme necessário
    menu_visivel = not menu_visivel

# Painel lateral
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="", font=("Arial", 16)).pack(pady=(20, 10))

def mostrar_tela_cadastro():
    global main_frame, chat_screen

    if chat_screen:
        chat_screen.pack_forget()
        # Alternativamente: chat_screen.destroy(); chat_screen = None

    main_frame.pack(fill="both", expand=True)



btn_cadastrar = ctk.CTkButton(sidebar, text="Cadastrar Paciente", anchor="w", fg_color="black", command=mostrar_tela_cadastro)
btn_cadastrar.pack(pady=10, padx=10, fill="x")

btn_relatorios = ctk.CTkButton(sidebar, text="Relatórios", fg_color="black", anchor="w", command=toggle_relatorio_menu)
btn_relatorios.pack(pady=10, padx=10, fill="x")


def mostrar_tela_chat():
    global main_frame, chat_screen

    main_frame.pack_forget()

    if not chat_screen:
        chat_screen = ChatScreen(app)

    chat_screen.pack(fill="both", expand=True)

btn_chat = ctk.CTkButton(sidebar, text="Chat", anchor="w", fg_color="black", command=mostrar_tela_chat)
btn_chat.pack(pady=10, padx=10, fill="x")

btn_logout = ctk.CTkButton(sidebar, text="Log out", anchor="w", fg_color="black")
btn_logout.pack(side="bottom", pady=20, padx=10, fill="x")

# Área de formulário principal
main_frame = ctk.CTkFrame(app, fg_color="#F0F0F0")  # cinza claro
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

ctk.CTkLabel(main_frame, text="Cadastro de Paciente", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="w")
ctk.CTkLabel(main_frame, text="Preencha os dados do paciente e o encaminhe para triagem").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 20))

# Campos do formulário
labels = ["Name", "CPF", "Telefone", "E-mail", "Data de Nascimento", "Sexo"]
entries = []

for i, label in enumerate(labels):
    ctk.CTkLabel(main_frame, text=label).grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")
    entry = ctk.CTkEntry(main_frame, width=250)
    entry.grid(row=i + 2, column=1, padx=10, pady=5, sticky="w")
    entries.append(entry)

labels_right = ["Tipo sanguíneo", "Endereco", "Status"]
entries_right = []

for i, label in enumerate(labels_right):
    ctk.CTkLabel(main_frame, text=label).grid(row=i + 2, column=2, padx=10, pady=5, sticky="w")
    entry = ctk.CTkEntry(main_frame, width=250)
    entry.grid(row=i + 2, column=3, padx=10, pady=5, sticky="w")
    entries_right.append(entry)

# Botão de salvar
save_button = ctk.CTkButton(main_frame, text="Salvar e encaminhar para triagem", fg_color="black")
save_button.grid(row=10, column=3, pady=40, sticky="e")

relatorio_menu = MenuRelatorios(app)
relatorio_menu.place_forget()

app.mainloop()
