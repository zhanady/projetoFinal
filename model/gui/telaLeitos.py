import customtkinter as ctk
from PIL import Image, ImageTk
import os
from banco.GerenciadorLeitos import *
from banco.GerenciadorPacientes import GerenciadorPacientes


class TelaLeitos(ctk.CTkFrame):
    def __init__(self, master, gerenciador_leitos, abrir_atendimento_callback=None, **kwargs):
        self.gerenciador_leitos = gerenciador_leitos
        super().__init__(master, fg_color="white", **kwargs)   
        self.abrir_atendimento_callback = abrir_atendimento_callback
        self.gerenciador_pacientes = GerenciadorPacientes()

        #tela = TelaLeitos(gerenciador_leitos=gerenciador)



        # Caminhos seguros para as imagens
        base_path = os.path.dirname(__file__)
        self.caminho_cama = os.path.join(base_path, "icons", "bed-single.png")
        self.caminho_paciente = os.path.join(base_path, "icons", "user.png")

        # Carregar imagens redimensionadas
        self.tk_cama = ImageTk.PhotoImage(Image.open(self.caminho_cama).resize((120, 120)))
        self.tk_paciente = None
        if os.path.exists(self.caminho_paciente):
            self.tk_paciente = ImageTk.PhotoImage(Image.open(self.caminho_paciente).resize((30, 30)))

        # Estado dos leitos
        self.leitos = self.carregar_leitos()


        self.criar_grid_leitos()

    def criar_grid_leitos(self):
        container = ctk.CTkFrame(self, fg_color="white")
        container.pack(expand=True)

        linhas, colunas = 2, 4
        for i in range(linhas):
            for j in range(colunas):
                idx = i * colunas + j
                if idx >= len(self.leitos):
                    continue

                leito = self.leitos[idx]
                frame_leito = ctk.CTkFrame(container, width=160, height=190, fg_color="white", corner_radius=10)
                frame_leito.grid(row=i, column=j, padx=30, pady=30)
                frame_leito.grid_propagate(False)

                # Canvas da cama
                canvas = ctk.CTkCanvas(frame_leito, width=120, height=120, bg="white", highlightthickness=0)
                canvas.pack()

                # Mostra cama
                canvas.create_image(60, 60, image=self.tk_cama)

                # Mostra personagem em cima da cama se estiver ocupado
                if leito["ocupado"] and self.tk_paciente:
                    canvas.create_image(60, 35, image=self.tk_paciente)

                # Clique no leito
                canvas.bind("<Button-1>", lambda e, i=idx: self.on_leito_click(i))

                # Nome do paciente
                nome_label = ctk.CTkLabel(
                    frame_leito,
                    text=leito["nome"] if leito["ocupado"] else "",
                    font=("Arial", 12),
                    text_color="black"
                )
                nome_label.pack(pady=5)

    def on_leito_click(self, idx):
        print(f"Leito {idx + 1} clicado")
        if self.abrir_atendimento_callback:
            self.abrir_atendimento_callback()
    
    def carregar_leitos(self):
        leitos_bd = self.gerenciador_leitos.consultar()
        
        # Ordena leitos pelo número (garante ordem fixa)
        leitos_bd = sorted(leitos_bd, key=lambda l: l.get("numero_leito", 0))

        leitos = []
        total_leitos = 8  # ou len(leitos_bd), se dinâmico

        for i in range(total_leitos):
            if i < len(leitos_bd):
                leito = leitos_bd[i]
                # ocupado = not leito["data_saida"]  # True se data_saida for None, "" ou False
                ocupado = leito["data_saida"]  # True se data_saida for None, "" ou False
                nome_paciente = ""
                paciente_id = None

                if ocupado and leito["id_paciente"]:
                    paciente_id = leito["id_paciente"]
                    paciente = self.gerenciador_pacientes.consultar({"id": paciente_id})
                    if paciente:
                        nome_paciente = paciente[0].get("nome", f"Paciente {paciente_id}")
                    else:
                        nome_paciente = f"Paciente {paciente_id}"

                leitos.append({
                    "ocupado": ocupado,
                    "nome": nome_paciente,
                    "id_paciente": paciente_id,
                    "numero_leito": leito.get("numero_leito", i + 1)  # opcional
                })
            else:
                # Leito vazio
                leitos.append({
                    "ocupado": False,
                    "nome": "",
                    "id_paciente": None,
                    "numero_leito": i + 1
                })

        return leitos


    def on_leito_click(self, idx):
        leito_info = self.leitos[idx]
        if leito_info["ocupado"] and leito_info["id_paciente"]:
            paciente_dados = self.gerenciador_pacientes.consultar({"id": leito_info["id_paciente"]})
            if paciente_dados:
                print(f"Abrindo atendimento para: {leito_info['nome']}")
                if self.abrir_atendimento_callback:
                    self.abrir_atendimento_callback(paciente_dados[0])
            else:
                print("Paciente não encontrado.")
        else:
            print("Leito disponível.")

