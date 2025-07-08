import customtkinter as ctk
from PIL import Image, ImageTk
import os
from banco.GerenciadorLeitos import *
from banco.GerenciadorPacientes import GerenciadorPacientes

class TelaLeitos(ctk.CTkFrame):
    def __init__(self, master, gerenciador_leitos, abrir_atendimento_callback=None, **kwargs):
        # Inicializa a classe base CTkFrame com cor de fundo branca
        super().__init__(master, fg_color="white", **kwargs)
        # Gerenciador de leitos (fornecido externamente)
        self.gerenciador_leitos = gerenciador_leitos
        # Callback para abrir atendimento ao clicar em um paciente
        self.abrir_atendimento_callback = abrir_atendimento_callback
        # Instância do gerenciador de pacientes
        self.gerenciador_pacientes = GerenciadorPacientes()

        # Define os caminhos das imagens usadas (ícone da cama e do paciente)
        base_path = os.path.dirname(__file__)
        self.caminho_cama = os.path.join(base_path, "icons", "bed-single.png")
        self.caminho_paciente = os.path.join(base_path, "icons", "user.png")

        # Carrega a imagem da cama redimensionada
        self.tk_cama = ImageTk.PhotoImage(Image.open(self.caminho_cama).resize((120, 120)))
        self.tk_paciente = None
        # Verifica se a imagem do paciente existe e carrega, se disponível
        if os.path.exists(self.caminho_paciente):
            self.tk_paciente = ImageTk.PhotoImage(Image.open(self.caminho_paciente).resize((30, 30)))

        # Carrega o estado atual dos leitos
        self.leitos = self.carregar_leitos()

        # Cria a visualização em grade (2 linhas × 4 colunas)
        self.criar_grid_leitos()

    def criar_grid_leitos(self):
        # Container principal para os leitos
        container = ctk.CTkFrame(self, fg_color="white")
        container.pack(expand=True)

        linhas, colunas = 2, 4  # Grade 2x4 = 8 leitos
        for i in range(linhas):
            for j in range(colunas):
                idx = i * colunas + j
                if idx >= len(self.leitos):
                    continue  # Evita erro se tiver menos de 8 leitos

                leito = self.leitos[idx]
                # Cada leito será representado por um frame fixo
                frame_leito = ctk.CTkFrame(container, width=160, height=190, fg_color="white", corner_radius=10)
                frame_leito.grid(row=i, column=j, padx=30, pady=30)
                frame_leito.grid_propagate(False)

                # Área visual da cama
                canvas = ctk.CTkCanvas(frame_leito, width=120, height=120, bg="white", highlightthickness=0)
                canvas.pack()

                # Desenha imagem da cama
                canvas.create_image(60, 60, image=self.tk_cama)

                # Se o leito está ocupado, mostra ícone do paciente
                if leito["ocupado"] and self.tk_paciente:
                    canvas.create_image(60, 35, image=self.tk_paciente)

                # Associa clique ao leito para mostrar atendimento
                canvas.bind("<Button-1>", lambda e, i=idx: self.on_leito_click(i))

                # Exibe nome do paciente se o leito estiver ocupado
                nome_label = ctk.CTkLabel(
                    frame_leito,
                    text=leito["nome"] if leito["ocupado"] else "",
                    font=("Arial", 12),
                    text_color="black"
                )
                nome_label.pack(pady=5)

    def on_leito_click(self, idx):
        """
        Função chamada ao clicar em um leito.
        Se estiver ocupado, chama o callback com os dados do paciente.
        """
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

    def carregar_leitos(self):
        """
        Consulta o banco de dados para carregar o estado dos leitos e
        os dados dos pacientes ocupando cada um.
        """
        leitos_bd = self.gerenciador_leitos.consultar()

        # Garante ordem dos leitos pelo número
        leitos_bd = sorted(leitos_bd, key=lambda l: l.get("numero_leito", 0))

        leitos = []
        total_leitos = 8  # Define número fixo de leitos (pode ser dinâmico)

        for i in range(total_leitos):
            if i < len(leitos_bd):
                leito = leitos_bd[i]
                # Um leito é ocupado se data_saida for None ou vazia
                ocupado = leito["data_saida"]
                nome_paciente = ""
                paciente_id = None

                # Se estiver ocupado, busca nome do paciente pelo ID
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
                    "numero_leito": leito.get("numero_leito", i + 1)
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
