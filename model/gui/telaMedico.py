import customtkinter as ctk
from projetoFinal.model.gui.telaFila import TelaFila
from projetoFinal.model.gui.telaChat import ChatScreen
from projetoFinal.model.gui.telaRelatorios import MenuRelatorios
from projetoFinal.model.gui.telaSolicitarRemedios import TelaSolicitarMedicamento
from projetoFinal.model.gui.telaLeitos import TelaLeitos
from projetoFinal.model.banco.GerenciadorPacientes import GerenciadorPacientes
from projetoFinal.model.banco.GerenciadorFila import GerenciadorFila
import tkinter.messagebox as msgbox
from banco.GerenciadorLeitos import GerenciadorLeitos
from datetime import datetime



class TelaMedico(ctk.CTkFrame):
    def __init__(self, master, paciente, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.paciente = paciente
        self.chat_screen = None
        self.gerenciador = GerenciadorPacientes()
        self.relatorio_menu = MenuRelatorios(self)
        self.gerenciador_leitos = GerenciadorLeitos()

        self.relatorio_menu.place_forget()
        self.menu_relatorio_visivel = False
        self.gerenciador_fila = GerenciadorFila()

        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.mostrar_atendimento()

    def limpar_area_principal(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        self.chat_screen = None

    def mostrar_atendimento(self):
        self.limpar_area_principal()

        content_frame = ctk.CTkFrame(self.area_principal, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = ctk.CTkFrame(content_frame, fg_color="#FAFAFA", corner_radius=8)
        top_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Dados
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

        # Sintomas
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

        # Histórico
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

        # Diagnóstico
        diagnostico_frame = ctk.CTkFrame(content_frame, fg_color="#FAFAFA", corner_radius=8)
        diagnostico_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(diagnostico_frame, text="Possível diagnóstico", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkLabel(diagnostico_frame, text="Descrição").pack(anchor="w", padx=10, pady=(5, 0))
        self.entrada_diagnostico = ctk.CTkEntry(diagnostico_frame, width=300)
        self.entrada_diagnostico.pack(anchor="w", padx=10)

        # Botões
        botoes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=10, pady=10)

        # Verificar se o paciente já está internado
        ja_internado = False
        try:
            todos_leitos = self.gerenciador_leitos.consultar({
                "id_paciente": self.paciente["id"]
            })
            for leito in todos_leitos:
                if not leito["data_saida"] or leito["data_saida"] in ("None", ""):
                    ja_internado = True
                    break
        except Exception as e:
            print(f"Erro ao verificar leito: {e}")


        # Botão Salvar
        ctk.CTkButton(
            botoes_frame,
            text="Salvar",
            fg_color="black",
            text_color="white",
            command=self.salvar_dados
        ).pack(side="right", padx=5)

        # Botão Internar (só se ainda não internado)
        if not ja_internado:
            ctk.CTkButton(
                botoes_frame,
                text="Internar",
                fg_color="black",
                text_color="white",
                command=self.internar_paciente
            ).pack(side="right", padx=5)

        # Botão Dar Alta
        ctk.CTkButton(
            botoes_frame,
            text="Dar alta",
            fg_color="black",
            text_color="white",
            command=self.dar_alta
        ).pack(side="right", padx=5)

        # Botão Solicitar Remédios
        ctk.CTkButton(
            botoes_frame,
            text="Solicitar remédios",
            fg_color="black",
            text_color="white",
            command=self.abrir_solicitacao_medicamento
        ).pack(side="right", padx=5)

    def internar_paciente(self):
        try:
            paciente_id = self.paciente.get("id")
            if not paciente_id:
                msgbox.showerror("Erro", "ID do paciente inválido.")
                return

            # Verifica se já está internado
            leitos_ativos = self.gerenciador_leitos.consultar({
                "id_paciente": paciente_id,
                "data_saida": None
            })
            if leitos_ativos:
                msgbox.showwarning("Já internado", "Este paciente já está em um leito.")
                return

            # 🧠 Buscar todos os leitos e verificar os ocupados
            todos_leitos = self.gerenciador_leitos.consultar()
            ocupados = {
                l["numero_leito"]
                for l in todos_leitos
                if not l["data_saida"] and l["numero_leito"] is not None
            }

            # Buscar o primeiro número de leito disponível (ex: de 1 a 8)
            total_leitos = 8  # pode ser dinâmico
            numero_disponivel = None
            for i in range(1, total_leitos + 1):
                if i not in ocupados:
                    numero_disponivel = i
                    break

            if numero_disponivel is None:
                msgbox.showwarning("Leitos ocupados", "Todos os leitos estão ocupados.")
                return

            # Dados da internação
            medico_id = 1  # Simulação
            data_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Inserir internação
            self.gerenciador_leitos.inserir(
                numero_leito=numero_disponivel,
                id_paciente=paciente_id,
                id_medico_encaminhou=medico_id,
                data_entrada=data_entrada
            )

            msgbox.showinfo("Internação", f"Paciente internado no leito {numero_disponivel}.")
            print(f"Paciente ID {paciente_id} internado no leito {numero_disponivel}.")

        except Exception as e:
            print(f"Erro ao internar paciente: {e}")
            msgbox.showerror("Erro", f"Erro ao internar paciente: {e}")
            
    def dar_alta(self):
        try:
            # Obter o ID correto do paciente
            paciente_id = self.paciente.get("id_paciente") or self.paciente.get("id")
            if not paciente_id:
                print("Paciente inválido (sem ID).")
                msgbox.showerror("Erro", "Paciente inválido (sem ID).")
                return

            # Verificar se o paciente existe no banco
            paciente_banco = self.gerenciador.consultar({"id": paciente_id})
            if not paciente_banco:
                print(f"Paciente ID {paciente_id} não encontrado no banco.")
                msgbox.showerror("Erro", f"Paciente ID {paciente_id} não encontrado no banco.")
                return

            # Atualizar o status do paciente para 'inativo'
            self.gerenciador.atualizar(id_paciente=paciente_id, novos_dados={"status": "inativo"})
            print("Status do paciente atualizado para inativo.")
            self.gerenciador.finalizar_ultimo_atendimento(paciente_id)


            # Remover da fila de atendimento médico (tipo_fila = 1)
            self.gerenciador_fila.remover_paciente_fila(paciente_id, tipo_fila=1)
            print("Paciente removido da fila de atendimento médico.")
            # Atualizar leito do paciente (liberar leito)
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
            self.master.master.mostrar_fila()  # Voltar para a tela de fila atualizada

        except Exception as e:
            print(f"Erro ao dar alta: {e}")
            msgbox.showerror("Erro", f"Erro ao dar alta: {e}")



    def salvar_dados(self):
        paciente_id = self.paciente.get("id")
       
        print(f"Tentando mover paciente ID {self.paciente['id']} para a fila de atendimento médico")
        
        if not self.gerenciador.paciente_existe(self.paciente["id"]):
            print(f"Erro: paciente ID {self.paciente['id']} não existe no banco!")
            return

        if not paciente_id:
            print("Paciente inválido (sem ID).")
            return

        # Verificar se o paciente realmente existe no banco
        paciente_banco = self.gerenciador.consultar({"id": paciente_id})
        if not paciente_banco:
            print(f"Paciente ID {paciente_id} não encontrado no banco.")
            msgbox.showerror("Erro", f"Paciente ID {paciente_id} não encontrado no banco.")
            return


        # Atualizar dados do paciente
        dados_atualizados = {campo: entry.get() for campo, entry in self.entries.items()}
        try:
            self.gerenciador.atualizar(id_paciente=self.paciente["id"], novos_dados=dados_atualizados)
            print("Dados do paciente atualizados com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar paciente: {e}")
            return

        # Registrar atendimento
        sintomas_selecionados = [s for s, var in self.sintomas_vars.items() if var.get()]
        sintomas_texto = ", ".join(sintomas_selecionados)
        descricao = self.entrada_descricao.get()
        diagnostico = self.entrada_diagnostico.get()

        if not diagnostico.strip():
            print("Diagnóstico não pode estar vazio.")
            msgbox.showwarning("Campo obrigatório", "O campo de diagnóstico não pode estar vazio.")
            return

        try:
            self.gerenciador.registrar_atendimento(
                paciente_id=self.paciente["id"],
                sintomas=sintomas_texto,
                descricao=descricao,
                diagnostico=diagnostico,
                status="em observação"
            )
            print("Atendimento registrado com sucesso!")

            # Mover para fila de atendimento médico
            id_paciente = self.paciente.get("id_paciente") or self.paciente.get("id")
            self.gerenciador_fila.remover_paciente_fila(id_paciente, tipo_fila=0)
            self.gerenciador_fila.adicionar_paciente_fila(id_paciente, tipo_fila=1, prioridade=3)


            # Pop-up de confirmação
            msgbox.showinfo(
                title="Atendimento salvo",
                message="Atendimento registrado com sucesso!\nPaciente movido para a fila de atendimento médico."
            )

            self.mostrar_atendimento()

        except Exception as e:
            print(f"Erro ao registrar atendimento ou mover de fila: {e}")
            msgbox.showerror("Erro", f"Ocorreu um erro: {e}")


    def mostrar_chat(self):
        self.limpar_area_principal()
        self.chat_screen = ChatScreen(self.area_principal)
        self.chat_screen.pack(fill="both", expand=True)

    def abrir_solicitacao_medicamento(self):
        TelaSolicitarMedicamento(self)

    def mostrar_relatorio(self, event):
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
        super().__init__(master, fg_color="white", **kwargs)

        self.menu_relatorio_visivel = False

        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#F8F9FA", border_width=1)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="My Account", font=("Arial", 16)).pack(pady=(20, 10))

        ctk.CTkButton(self.sidebar, text="Fila", fg_color="black", anchor="w", command=self.mostrar_fila).pack(padx=10, pady=5, fill="x")
        #ctk.CTkButton(self.sidebar, text="Atendimento", fg_color="black", anchor="w", command=self.mostrar_atendimento).pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Chat", fg_color="black", anchor="w", command=self.mostrar_chat).pack(padx=10, pady=5, fill="x")
        self.btn_leitos = ctk.CTkButton(self.sidebar, anchor="w", text="Leitos", fg_color="black", command=self.mostrar_leitos )
        self.btn_leitos.pack(padx=10, pady=5, fill="x")

        btn_relatorios = ctk.CTkButton(self.sidebar, text="Relatórios", fg_color="black", anchor="w")
        btn_relatorios.pack(padx=10, pady=5, fill="x")
        btn_relatorios.bind("<Button-1>", self.mostrar_relatorio)

        ctk.CTkButton(self.sidebar, text="Log out", fg_color="black", anchor="w", command=self.quit).pack(side="bottom", padx=10, pady=20, fill="x")

        self.area_principal = ctk.CTkFrame(self, fg_color="white")
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.menu_relatorio = MenuRelatorios(self)
        self.menu_relatorio.place_forget()

        self.mostrar_fila()

    def limpar_area_principal(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def mostrar_fila(self):
        self.limpar_area_principal()
        tela = TelaFila(self.area_principal, abrir_atendimento_callback=self.mostrar_atendimento)
        tela.pack(fill="both", expand=True)
    
    def mostrar_leitos(self):
        self.limpar_area_principal()

        def abrir_atendimento(paciente):
            self.mostrar_atendimento(paciente)

        gerenciador = GerenciadorLeitos()

        tela = TelaLeitos(
            master=self.area_principal,
            gerenciador_leitos=gerenciador,
            abrir_atendimento_callback=abrir_atendimento
        )
        tela.pack(fill="both", expand=True)





    def mostrar_atendimento(self, paciente):
        self.limpar_area_principal()
        tela = TelaMedico(self.area_principal, paciente=paciente)
        tela.pack(fill="both", expand=True)

    def mostrar_chat(self):
        self.limpar_area_principal()
        tela = ChatScreen(self.area_principal)
        tela.pack(fill="both", expand=True)

    def mostrar_relatorio(self, event):
        if self.menu_relatorio_visivel:
            self.menu_relatorio.place_forget()
            self.menu_relatorio_visivel = False
        else:
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            self.menu_relatorio.place(x=x + 10, y=y + 10)
            self.menu_relatorio_visivel = True


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Sistema Hospitalar")
    app.geometry("1200x700")

    tela = TelaPrincipal(app)
    tela.pack(fill="both", expand=True)

    app.mainloop()
