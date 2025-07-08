# Importações de bibliotecas e módulos do sistema
import customtkinter as ctk  # Interface gráfica moderna baseada em Tkinter
from gui.telaFila import TelaFila
from gui.telaChat import ChatScreen
from gui.telaRelatorios import MenuRelatorios
from gui.telaSolicitarRemedios import TelaSolicitarMedicamento
from gui.telaLeitos import TelaLeitos
from banco.GerenciadorPacientes import GerenciadorPacientes
from banco.GerenciadorFila import GerenciadorFila
import tkinter.messagebox as msgbox
from banco.GerenciadorLeitos import GerenciadorLeitos
from datetime import datetime, timedelta

from sistemaemergencial.Triagem import Triagem  # Enum com as cores de triagem hospitalar


# Classe principal da interface do médico
class TelaMedico(ctk.CTkFrame):
    def __init__(self, master, paciente, **kwargs):
        # Inicializa a tela principal do médico, passando os dados do paciente selecionado
        super().__init__(master, fg_color="white", **kwargs)
        self.paciente = paciente  # Dicionário com dados do paciente atual
        self.chat_screen = None  # Inicializa o chat como inativo
        self.gerenciador = GerenciadorPacientes()  # Gerencia dados do paciente
        self.relatorio_menu = MenuRelatorios(self)  # Menu de relatórios
        self.gerenciador_leitos = GerenciadorLeitos()  # Gerencia os leitos hospitalares

        # Oculta o menu de relatórios por padrão
        self.relatorio_menu.place_forget()
        self.menu_relatorio_visivel = False

        self.gerenciador_fila = GerenciadorFila()  # Gerencia a fila de pacientes

        # Cria área central da tela onde os elementos principais serão mostrados
        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        # Chama a função que monta a tela de atendimento
        self.mostrar_atendimento()

    def limpar_area_principal(self):
        # Remove todos os widgets da área principal (usado para mudar de tela)
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        self.chat_screen = None

    def mostrar_atendimento(self):
        # Monta a interface de atendimento ao paciente, com dados, sintomas, diagnóstico etc.
        self.limpar_area_principal()

        content_frame = ctk.CTkFrame(self.area_principal, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = ctk.CTkFrame(content_frame, fg_color="#FAFAFA", corner_radius=8)
        top_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # ---------- DADOS DO PACIENTE ----------
        dados_frame = ctk.CTkFrame(top_frame, fg_color="white")
        dados_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        ctk.CTkLabel(dados_frame, text="Dados", font=("Arial", 14, "bold")).pack(anchor="w")
        self.entries = {}
        campos = [("Nome", "nome"), ("Data de nascimento", "data_nascimento"), ("Sexo", "sexo"), ("Status", "status")]
        for label, chave in campos:
            ctk.CTkLabel(dados_frame, text=label).pack(anchor="w", padx=5, pady=(5, 0))
            entry = ctk.CTkEntry(dados_frame, width=200)
            entry.insert(0, self.paciente.get(chave, ""))
            entry.pack(anchor="w", padx=5)
            self.entries[chave] = entry

        # ---------- SINTOMAS ----------
        sintomas_frame = ctk.CTkFrame(top_frame, fg_color="white")
        sintomas_frame.pack(side="left", fill="both", expand=True, padx=(5, 5), pady=10)

        ctk.CTkLabel(sintomas_frame, text="Sintomas", font=("Arial", 14, "bold")).pack(anchor="w", padx=5)
        self.sintomas_vars = {}
        for sintoma in ["Febre", "Tosse", "Dor de garganta"]:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(sintomas_frame, text=sintoma, variable=var).pack(anchor="w", padx=5)
            self.sintomas_vars[sintoma] = var

        ctk.CTkLabel(sintomas_frame, text="Descrição").pack(anchor="w", padx=5, pady=(5, 0))
        self.entrada_descricao = ctk.CTkEntry(sintomas_frame, width=200)
        self.entrada_descricao.pack(anchor="w", padx=5)

        # ---------- HISTÓRICO ----------
        historico_frame = ctk.CTkFrame(top_frame, fg_color="white", border_width=1, corner_radius=8)
        historico_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        ctk.CTkLabel(historico_frame, text="Histórico do Paciente", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        historico = self.gerenciador.obter_historico_paciente(self.paciente["id"])
        if historico:
            for item in historico:
                texto = f"{item['data']} - {item['diagnostico']} ({item['status']})"
                ctk.CTkLabel(historico_frame, text=f"• {texto}").pack(anchor="w", padx=10, pady=2)
        else:
            ctk.CTkLabel(historico_frame, text="Nenhum histórico encontrado.").pack(anchor="w", padx=10, pady=2)

        # ---------- DIAGNÓSTICO E TRIAGEM ----------
        diagnostico_frame = ctk.CTkFrame(content_frame, fg_color="#FAFAFA", corner_radius=8)
        diagnostico_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(diagnostico_frame, text="Possível diagnóstico", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkLabel(diagnostico_frame, text="Descrição").pack(anchor="w", padx=10, pady=(5, 0))
        self.entrada_diagnostico = ctk.CTkEntry(diagnostico_frame, width=300)
        self.entrada_diagnostico.pack(anchor="w", padx=10)

        # Mostra o valor da triagem do paciente (cor)
        texto_triagem = "Triagem: "
        valor_triagem = self.gerenciador.get_triagem(self.paciente["id"])
        if valor_triagem == Triagem.VERMELHA:
            texto_triagem += "Vermelha"
        elif valor_triagem == Triagem.LARANJA:
            texto_triagem += "Laranja"
        elif valor_triagem == Triagem.AMARELA:
            texto_triagem += "Amarela"
        elif valor_triagem == Triagem.VERDE:
            texto_triagem += "Verde"
        else:
            texto_triagem += "Azul"
        ctk.CTkLabel(diagnostico_frame, text=texto_triagem).pack(anchor="w", padx=10, pady=(5, 0))

        # Mostra o tempo restante estimado de internação (caso esteja internado)
        if self.gerenciador_leitos.isEmLeito(self.paciente["id"]):
            leito = self.gerenciador_leitos.get_leito(self.paciente["id"])
            data_saida = leito.get_data_saida()
            data_atual = datetime.now()
            periodo = data_saida - data_atual
            horas = str(int(periodo.total_seconds() // 3600))
            minutos = str(int(periodo.total_seconds() % 3600) // 60)
            segundos = int(periodo.total_seconds() % 60)
            if segundos < 10:
                segundos = "0" + str(segundos)
            else:
                segundos = str(segundos)
            ctk.CTkLabel(diagnostico_frame, text="Tempo estimado de saída: " + horas + ":" + minutos + ":" + segundos).pack(anchor="w", padx=10, pady=(5, 0))

        # ---------- BOTÕES ----------
        botoes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=10, pady=10)

        # Verifica se o paciente já está internado
        ja_internado = False
        try:
            todos_leitos = self.gerenciador_leitos.consultar({"id_paciente": self.paciente["id"]})
            for leito in todos_leitos:
                if not leito["data_saida"] or leito["data_saida"] in ("None", ""):
                    ja_internado = True
                    break
        except Exception as e:
            print(f"Erro ao verificar leito: {e}")

        # Botão para salvar dados e registrar atendimento
        ctk.CTkButton(botoes_frame, text="Salvar", fg_color="black", text_color="white", command=self.salvar_dados).pack(side="right", padx=5)

        # Botão para internar o paciente (se ainda não internado)
        if not ja_internado:
            ctk.CTkButton(botoes_frame, text="Internar", fg_color="black", text_color="white", command=self.internar_paciente).pack(side="right", padx=5)

        # Botão para dar alta ao paciente
        ctk.CTkButton(botoes_frame, text="Dar alta", fg_color="black", text_color="white", command=self.dar_alta).pack(side="right", padx=5)

        # Botão para solicitar medicamentos
        ctk.CTkButton(botoes_frame, text="Solicitar remédios", fg_color="black", text_color="white", command=self.abrir_solicitacao_medicamento).pack(side="right", padx=5)

    def internar_paciente(self):
        try:
            paciente_id = self.paciente.get("id")
            if not paciente_id:
                msgbox.showerror("Erro", "ID do paciente inválido.")
                return

            # Verifica se o paciente já está internado
            leitos_ativos = self.gerenciador_leitos.consultar({
                "id_paciente": paciente_id,
                "data_saida": None
            })
            if leitos_ativos or self.gerenciador_leitos.isEmLeito(paciente_id):
                msgbox.showwarning("Já internado", "Este paciente já está em um leito.")
                return

            # Busca todos os leitos e determina quais estão ocupados
            todos_leitos = self.gerenciador_leitos.consultar()
            ocupados = {
                l["numero_leito"]
                for l in todos_leitos
                if not l["data_saida"] and l["numero_leito"] is not None
            }

            # Procura o primeiro leito livre de 1 a 8
            total_leitos = 8
            numero_disponivel = None
            for i in range(1, total_leitos + 1):
                if i not in ocupados:
                    numero_disponivel = i
                    break

            if numero_disponivel is None:
                msgbox.showwarning("Leitos ocupados", "Todos os leitos estão ocupados.")
                return

            # Define o tempo de permanência conforme triagem
            medico_id = 1  # Simulado
            data_entrada = datetime.now()
            valor_triagem = self.gerenciador.get_triagem(paciente_id)

            if valor_triagem == Triagem.VERMELHA:
                data_saida = (data_entrada + timedelta(hours=3)) \
                    .strftime("%Y-%m-%d %H:%M:%S")
            elif valor_triagem == Triagem.LARANJA:
                data_saida = (data_entrada + timedelta(hours=1, minutes=30)) \
                    .strftime("%Y-%m-%d %H:%M:%S")
            elif valor_triagem == Triagem.AMARELA:
                data_saida = (data_entrada + timedelta(minutes=45)) \
                    .strftime("%Y-%m-%d %H:%M:%S")
            elif valor_triagem == Triagem.VERDE:
                data_saida = (data_entrada + timedelta(minutes=25)) \
                    .strftime("%Y-%m-%d %H:%M:%S")
            else:
                data_saida = (data_entrada + timedelta(minutes=12)) \
                    .strftime("%Y-%m-%d %H:%M:%S")

            # Formata datas para string
            data_entrada = data_entrada.strftime("%Y-%m-%d %H:%M:%S")
            # Registra a internação no banco
            self.gerenciador_leitos.inserir(
                numero_leito=numero_disponivel,
                id_paciente=paciente_id,
                id_medico_encaminhou=medico_id,
                data_entrada=data_entrada,
                data_saida=data_saida
            )

            msgbox.showinfo("Internação", f"Paciente internado no leito {numero_disponivel}.")
            print(f"Paciente ID {paciente_id} internado no leito {numero_disponivel}.")

        except Exception as e:
            print(f"Erro ao internar paciente: {e}")
            msgbox.showerror("Erro", f"Erro ao internar paciente: {e}")

    def dar_alta(self):
        try:
            # Obtém o ID do paciente
            paciente_id = self.paciente.get("id_paciente") or self.paciente.get("id")
            if not paciente_id:
                msgbox.showerror("Erro", "Paciente inválido (sem ID).")
                return

            # Verifica se o paciente existe
            paciente_banco = self.gerenciador.consultar({"id": paciente_id})
            if not paciente_banco:
                msgbox.showerror("Erro", f"Paciente ID {paciente_id} não encontrado no banco.")
                return

            # Atualiza status para "inativo" e finaliza o atendimento
            self.gerenciador.atualizar(id_paciente=paciente_id, novos_dados={"status": "inativo"})
            self.gerenciador.finalizar_ultimo_atendimento(paciente_id)
            self.gerenciador.limpar_triagens(paciente_id)

            # Remove paciente das filas (geral e médica)
            self.gerenciador_fila.remover_paciente_fila(paciente_id, tipo_fila=1)
            self.gerenciador_fila.remover_paciente_fila(paciente_id, tipo_fila=0)

            # Libera o leito se estiver internado
            if self.gerenciador_leitos.isEmLeito(paciente_id):
                self.gerenciador_leitos.remover_por_paciente(paciente_id)

            # Atualiza a data de saída no leito (se ainda não foi definido)
            try:
                leitos_ativos = self.gerenciador_leitos.consultar({"id_paciente": paciente_id})
                for leito in leitos_ativos:
                    if not leito["data_saida"] or leito["data_saida"] in ("None", ""):
                        self.gerenciador_leitos.atualizar(
                            id_leito=leito["id"],
                            novos_dados={"data_saida": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        )
                        print(f"Leito ID {leito['id']} liberado.")
                        break
            except Exception as e:
                print(f"Erro ao liberar leito: {e}")

            msgbox.showinfo("Alta concluída", "Paciente recebeu alta com sucesso e foi removido da fila.")
            self.master.master.mostrar_fila()  # Retorna à tela da fila de pacientes

        except Exception as e:
            print(f"Erro ao dar alta: {e}")
            msgbox.showerror("Erro", f"Erro ao dar alta: {e}")

    def salvar_dados(self):
        paciente_id = self.paciente.get("id")
        print(f"Tentando mover paciente ID {self.paciente['id']} para a fila de atendimento médico")

        if not self.gerenciador.paciente_existe(self.paciente["id"]):
            print(f"Erro: paciente ID {self.paciente['id']} não existe no banco!")
            return

        # Valida ID
        if not paciente_id:
            print("Paciente inválido (sem ID).")
            return

        paciente_banco = self.gerenciador.consultar({"id": paciente_id})
        if not paciente_banco:
            msgbox.showerror("Erro", f"Paciente ID {paciente_id} não encontrado no banco.")
            return

        # Atualiza os dados de entrada (nome, data de nascimento, sexo, status)
        dados_atualizados = {campo: entry.get() for campo, entry in self.entries.items()}
        try:
            self.gerenciador.atualizar(id_paciente=paciente_id, novos_dados=dados_atualizados)
            print("Dados do paciente atualizados com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar paciente: {e}")
            return

        # Captura sintomas selecionados e o diagnóstico
        sintomas_selecionados = [s for s, var in self.sintomas_vars.items() if var.get()]
        sintomas_texto = ", ".join(sintomas_selecionados)
        descricao = self.entrada_descricao.get()
        diagnostico = self.entrada_diagnostico.get()

        if not diagnostico.strip():
            msgbox.showwarning("Campo obrigatório", "O campo de diagnóstico não pode estar vazio.")
            return

        try:
            # Registra o atendimento no histórico do paciente
            self.gerenciador.registrar_atendimento(
                paciente_id=paciente_id,
                sintomas=sintomas_texto,
                descricao=descricao,
                diagnostico=diagnostico,
                status="em observação"
            )
            print("Atendimento registrado com sucesso!")

            # Move paciente para fila de atendimento médico (tipo_fila = 1)
            self.gerenciador_fila.remover_paciente_fila(paciente_id, tipo_fila=0)
            self.gerenciador_fila.adicionar_paciente_fila(paciente_id, tipo_fila=1, prioridade=3)

            # Exibe confirmação e atualiza tela
            msgbox.showinfo(
                title="Atendimento salvo",
                message="Atendimento registrado com sucesso!\nPaciente movido para a fila de atendimento médico."
            )
            self.mostrar_atendimento()

        except Exception as e:
            print(f"Erro ao registrar atendimento ou mover de fila: {e}")
            msgbox.showerror("Erro", f"Ocorreu um erro: {e}")

    def mostrar_chat(self):
        # Troca a tela principal para o chat
        self.limpar_area_principal()
        self.chat_screen = ChatScreen(self.area_principal)
        self.chat_screen.pack(fill="both", expand=True)

    def abrir_solicitacao_medicamento(self):
        # Abre a janela de solicitação de medicamento (como Toplevel)
        TelaSolicitarMedicamento(self)

    def mostrar_relatorio(self, event):
        # Alterna visibilidade do menu de relatórios na tela do médico
        if self.menu_relatorio_visivel:
            self.relatorio_menu.place_forget()
            self.menu_relatorio_visivel = False
        else:
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            self.relatorio_menu.place(x=x + 10, y=y + 10)
            self.menu_relatorio_visivel = True


class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Inicializa o frame principal da aplicação
        super().__init__(master, fg_color="white", **kwargs)

        self.menu_relatorio_visivel = False  # Controla a visibilidade do menu de relatórios

        # Cria a barra lateral (menu)
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#F8F9FA", border_width=1)
        self.sidebar.pack(side="left", fill="y")

        # Título da barra lateral
        ctk.CTkLabel(self.sidebar, text="My Account", font=("Arial", 16)).pack(pady=(20, 10))

        # Botão para acessar a fila de pacientes
        ctk.CTkButton(self.sidebar, text="Fila", fg_color="black", anchor="w", command=self.mostrar_fila).pack(
            padx=10, pady=5, fill="x")

        # Botão para abrir o chat
        ctk.CTkButton(self.sidebar, text="Chat", fg_color="black", anchor="w", command=self.mostrar_chat).pack(
            padx=10, pady=5, fill="x")

        # Botão para visualizar leitos
        self.btn_leitos = ctk.CTkButton(self.sidebar, anchor="w", text="Leitos", fg_color="black",
                                        command=self.mostrar_leitos)
        self.btn_leitos.pack(padx=10, pady=5, fill="x")

        # Botão de relatórios com evento de clique vinculado
        btn_relatorios = ctk.CTkButton(self.sidebar, text="Relatórios", fg_color="black", anchor="w")
        btn_relatorios.pack(padx=10, pady=5, fill="x")
        btn_relatorios.bind("<Button-1>", self.mostrar_relatorio)

        # Botão para logout (finaliza o app)
        ctk.CTkButton(self.sidebar, text="Log out", fg_color="black", anchor="w", command=self.quit).pack(
            side="bottom", padx=10, pady=20, fill="x")

        # Área principal onde o conteúdo das telas será renderizado
        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        # Menu de relatórios oculto inicialmente
        self.menu_relatorio = MenuRelatorios(self)
        self.menu_relatorio.place_forget()

        # Exibe a fila como tela inicial
        self.mostrar_fila()

    def limpar_area_principal(self):
        # Remove todos os widgets da área principal antes de trocar de tela
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def mostrar_fila(self):
        # Mostra a tela da fila de pacientes
        self.limpar_area_principal()
        tela = TelaFila(self.area_principal, abrir_atendimento_callback=self.mostrar_atendimento)
        tela.pack(fill="both", expand=True)

    def mostrar_leitos(self):
        # Mostra a tela de leitos
        self.limpar_area_principal()

        def abrir_atendimento(paciente):
            # Função usada dentro da tela de leitos para redirecionar ao atendimento do paciente
            self.mostrar_atendimento(paciente)

        gerenciador = GerenciadorLeitos()  # Instância para gerenciar dados dos leitos

        tela = TelaLeitos(
            master=self.area_principal,
            gerenciador_leitos=gerenciador,
            abrir_atendimento_callback=abrir_atendimento
        )
        tela.pack(fill="both", expand=True)

    def mostrar_atendimento(self, paciente):
        # Mostra a tela de atendimento médico para um paciente específico
        self.limpar_area_principal()
        tela = TelaMedico(self.area_principal, paciente=paciente)
        tela.pack(fill="both", expand=True)

    def mostrar_chat(self):
        # Mostra a tela de chat
        self.limpar_area_principal()
        tela = ChatScreen(self.area_principal)
        tela.pack(fill="both", expand=True)

    def mostrar_relatorio(self, event):
        # Mostra ou oculta o menu de relatórios, dependendo do estado atual
        if self.menu_relatorio_visivel:
            self.menu_relatorio.place_forget()
            self.menu_relatorio_visivel = False
        else:
            # Posiciona o menu próximo ao local do clique
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            self.menu_relatorio.place(x=x + 10, y=y + 10)
            self.menu_relatorio_visivel = True


# Ponto de entrada do programa
if __name__ == "__main__":
    # Define aparência e tema
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Cria janela principal da aplicação
    app = ctk.CTk()
    app.title("Sistema Hospitalar")
    app.geometry("1200x700")

    # Instancia e exibe a TelaPrincipal
    tela = TelaPrincipal(app)
    tela.pack(fill="both", expand=True)

    # Inicia o loop principal da interface
    app.mainloop()
