import customtkinter as ctk
from PIL import Image
import os
from banco.GerenciadorFila import GerenciadorFila
from banco.GerenciadorPacientes import *

class TelaFila(ctk.CTkFrame):
    def __init__(self, master, abrir_atendimento_callback=None, **kwargs):
        """
        Tela que exibe as filas de triagem e de atendimento médico.
        Permite interação com os pacientes listados.
        """
        super().__init__(master, fg_color="white", **kwargs)
        self.gerenciador_fila = GerenciadorFila()  # Gerencia as filas do sistema
        self.abrir_atendimento_callback = abrir_atendimento_callback  # Função chamada ao clicar no paciente

        # Título da seção de triagem
        self.label_triagem = ctk.CTkLabel(self, text="Fila triagem", font=("Arial", 18, "bold"), text_color="black")
        self.label_triagem.pack(pady=(20, 0), anchor="w", padx=30)

        # Link clicável para detalhes (pode ser substituído futuramente por funcionalidade real)
        self.link_triagem = ctk.CTkLabel(self, text="Clique para mais detalhes", text_color="blue", cursor="hand2")
        self.link_triagem.pack(anchor="w", padx=30)
        self.link_triagem.bind("<Button-1>", lambda e: print("Detalhes triagem"))

        # Container visual que exibe os pacientes na fila de triagem
        self.container_triagem = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10)
        self.container_triagem.pack(fill="x", padx=30, pady=(10, 20))

        # Título da seção de atendimento
        self.label_atendimento = ctk.CTkLabel(self, text="Fila atendimento médico", font=("Arial", 18, "bold"), text_color="black")
        self.label_atendimento.pack(anchor="w", padx=30)

        # Link clicável para detalhes da fila de atendimento
        self.link_atendimento = ctk.CTkLabel(self, text="Clique para mais detalhes", text_color="blue", cursor="hand2")
        self.link_atendimento.pack(anchor="w", padx=30)
        self.link_atendimento.bind("<Button-1>", lambda e: print("Detalhes atendimento"))

        # Container visual para fila de atendimento
        self.container_atendimento = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10)
        self.container_atendimento.pack(fill="x", padx=30, pady=(10, 20))

        # Ícone de avatar (imagem do paciente simulada)
        self.avatar_img = ctk.CTkImage(light_image=Image.open("icons/user.png"), size=(50, 50))

        self.atualizar_fila()  # Carrega os dados das filas ao iniciar

    def atualizar_fila(self):
        """
        Atualiza os dados das duas filas (triagem e atendimento).
        Limpa os containers e recria os elementos visuais com base no banco de dados.
        """
        # Limpa os dois containers
        for container in [self.container_triagem, self.container_atendimento]:
            for widget in container.winfo_children():
                widget.destroy()

        # Busca as filas no banco
        fila_triagem = self.gerenciador_fila.buscar_fila(tipo_fila=0)
        fila_atendimento = self.gerenciador_fila.buscar_fila(tipo_fila=1)

        # Preenche os containers com os pacientes
        self._preencher_container(self.container_triagem, fila_triagem)
        self._preencher_container(self.container_atendimento, fila_atendimento)

    def _preencher_container(self, container, fila):
        """
        Adiciona os cards de pacientes em um container da fila.

        Args:
            container (CTkFrame): Frame visual que receberá os pacientes.
            fila: objeto de fila com método get_pacientes().
        """
        frame_linha = ctk.CTkFrame(container, fg_color="#F5F5F5")
        frame_linha.pack(pady=10, padx=10, anchor="w")

        pacientes = fila.get_pacientes()

        for paciente in pacientes:
            frame_paciente = ctk.CTkFrame(frame_linha, fg_color="white", corner_radius=8, width=100)
            frame_paciente.pack(side="left", padx=10, pady=5)

            nome = paciente.get_nome()  # Obtém nome do paciente a partir do objeto

            # Imagem de avatar
            ctk.CTkLabel(frame_paciente, image=self.avatar_img, text="").pack(pady=(10, 5))

            # Botão com o nome do paciente
            ctk.CTkButton(
                frame_paciente,
                text=nome,
                font=("Arial", 12),
                fg_color="transparent",
                text_color="black",
                hover_color="#E0E0E0",
                command=lambda p=paciente: self.mostrar_atendimento(p)
            ).pack(pady=(0, 10))

    def mostrar_atendimento(self, paciente):
        """
        Ao clicar em um paciente, chama o callback com os dados completos do banco.

        Args:
            paciente: objeto paciente da fila.
        """
        if self.abrir_atendimento_callback:
            paciente_id = paciente.get_id()
            if not paciente_id:
                print(f"[ERRO] Paciente não tem ID válido: {paciente}")
                return

            gerenciador = GerenciadorPacientes()
            paciente_completo = gerenciador.consultar(filtros={"id": paciente_id})

            if paciente_completo:
                self.abrir_atendimento_callback(paciente_completo[0])
            else:
                print(f"[ERRO] Paciente ID {paciente_id} não encontrado no banco.")
