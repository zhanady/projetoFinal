import customtkinter as ctk
from PIL import Image
import os
from banco.GerenciadorFila import GerenciadorFila
from banco.GerenciadorPacientes import *


class TelaFila(ctk.CTkFrame):
    def __init__(self, master, abrir_atendimento_callback=None, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.gerenciador_fila = GerenciadorFila()
        self.abrir_atendimento_callback = abrir_atendimento_callback

        self.label_triagem = ctk.CTkLabel(self, text="Fila triagem", font=("Arial", 18, "bold"), text_color="black")
        self.label_triagem.pack(pady=(20, 0), anchor="w", padx=30)

        self.link_triagem = ctk.CTkLabel(self, text="Clique para mais detalhes", text_color="blue", cursor="hand2")
        self.link_triagem.pack(anchor="w", padx=30)
        self.link_triagem.bind("<Button-1>", lambda e: print("Detalhes triagem"))

        self.container_triagem = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10)
        self.container_triagem.pack(fill="x", padx=30, pady=(10, 20))

        self.label_atendimento = ctk.CTkLabel(self, text="Fila atendimento médico", font=("Arial", 18, "bold"), text_color="black")
        self.label_atendimento.pack(anchor="w", padx=30)

        self.link_atendimento = ctk.CTkLabel(self, text="Clique para mais detalhes", text_color="blue", cursor="hand2")
        self.link_atendimento.pack(anchor="w", padx=30)
        self.link_atendimento.bind("<Button-1>", lambda e: print("Detalhes atendimento"))

        self.container_atendimento = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10)
        self.container_atendimento.pack(fill="x", padx=30, pady=(10, 20))

        self.avatar_img = ctk.CTkImage(light_image=Image.open("model/gui/icons/user.png"), size=(50, 50))
        self.atualizar_fila()

    def atualizar_fila(self):
        for container in [self.container_triagem, self.container_atendimento]:
            for widget in container.winfo_children():
                widget.destroy()

        pacientes_triagem = self.gerenciador_fila.buscar_fila(tipo_fila=0)
        pacientes_atendimento = self.gerenciador_fila.buscar_fila(tipo_fila=1)
        print(pacientes_triagem)
        self._preencher_container(self.container_triagem, pacientes_triagem)
        self._preencher_container(self.container_atendimento, pacientes_atendimento)

    def _preencher_container(self, container, pacientes):
        frame_linha = ctk.CTkFrame(container, fg_color="#F5F5F5")
        frame_linha.pack(pady=10, padx=10, anchor="w")

        for paciente in pacientes:
            frame_paciente = ctk.CTkFrame(frame_linha, fg_color="white", corner_radius=8, width=100)
            frame_paciente.pack(side="left", padx=10, pady=5)

            nome = paciente.get("nome", paciente['nome_paciente'])

            ctk.CTkLabel(frame_paciente, image=self.avatar_img, text="").pack(pady=(10, 5))
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
        if self.abrir_atendimento_callback:
            paciente_id = paciente.get("id") or paciente.get("id_paciente")
            if not paciente_id:
                print(f"[ERRO] Paciente não tem ID válido: {paciente}")
                return

            gerenciador = GerenciadorPacientes()
            id_paciente = paciente.get("id_paciente") or paciente.get("id")
            paciente_completo = gerenciador.consultar(filtros={"id": id_paciente})

            if paciente_completo:
                self.abrir_atendimento_callback(paciente_completo[0])
            else:
                print(f"[ERRO] Paciente ID {paciente_id} não encontrado no banco.")
