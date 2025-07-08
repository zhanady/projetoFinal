import datetime
import sqlite3
from typing import Optional, Dict, Any, List
from banco.GerenciadorFila import *
from datetime import datetime, timedelta


class GerenciadorPacientes:
    def __init__(self, db_name: str = '../hospital.db'):
        """
        Inicializa o gerenciador de pacientes com acesso ao banco de dados.
        
        Args:
            db_name (str): Caminho para o banco de dados SQLite.
        """
        self.db_name = db_name
        self._criar_tabelas()
        self.gerenciadorFila = GerenciadorFila()  # Gerencia a fila de atendimento

    def _conectar(self):
        """Estabelece conexão com o banco de dados."""
        return sqlite3.connect(self.db_name)

    def _criar_tabelas(self):
        """
            Cria as tabelas necessárias para o funcionamento da lógica dos pacientes:
            primeiro cria a tabela de triagem, depois a tabela de pacientes e por fim
            a tabela de histórico
        """
        with self._conectar() as conn:
            cursor = conn.cursor()

            # Tabela de pacientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    data_nascimento TEXT,
                    sexo TEXT,
                    tipo_sanguineo TEXT,
                    endereco TEXT,
                    status TEXT NOT NULL DEFAULT 'ativo'
                );
            ''')

            # Tabela de triagens
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS triagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paciente_id INTEGER,
                    escala_dor INTEGER NOT NULL,
                    escala_glascow INTEGER NOT NULL,
                    sinais_vitais INTEGER NOT NULL,
                    CONSTRAINT triagemPaciente FOREIGN KEY (paciente_id) 
                    REFERENCES pacientes (id)
                );
            ''')

            # Tabela de histórico de atendimentos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_atendimentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paciente_id INTEGER NOT NULL,
                    usuario_id INTEGER,
                    data TEXT NOT NULL,
                    sintomas TEXT,
                    descricao TEXT,
                    diagnostico TEXT,
                    status TEXT DEFAULT 'pendente'
                );
            ''')

            conn.commit()

    def paciente_existe(self, id_paciente):
        """Verifica se o paciente existe no banco."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM pacientes WHERE id = ?", (id_paciente,))
            return cursor.fetchone() is not None

    def cadastrar_ou_reativar(self, nome, cpf, telefone, email, data_nascimento, sexo,
                              tipo_sanguineo, endereco, escala_dor, escala_glascow, sinais_vitais):
        """
        Cadastra um novo paciente ou reativa um paciente inativo.
        Também registra a triagem e, se necessário, o insere na fila ou leito.

        Retorna:
            int: ID do paciente
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, status FROM pacientes WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()

            if resultado:
                paciente_id, status_atual = resultado

                # Se já existe e está inativo, reativa e registra nova triagem
                if status_atual.lower() == "inativo":
                    cursor.execute("UPDATE pacientes SET status = 'ativo' WHERE id = ?", (paciente_id,))

                    cursor.execute('''
                        INSERT INTO triagens (paciente_id, escala_dor, escala_glascow, sinais_vitais) 
                        VALUES (?, ?, ?, ?)
                    ''', (paciente_id, escala_dor, escala_glascow, sinais_vitais))
                    conn.commit()

                    print(f"Paciente com CPF {cpf} reativado.")

                    if not self.verificar_triagem_vermelha(paciente_id, escala_dor,
                                                           escala_glascow, sinais_vitais):
                        self.gerenciadorFila.adicionar_paciente_fila(id_paciente=paciente_id, tipo_fila=0, prioridade=3)
                else:
                    print(f"Paciente com CPF {cpf} já está ativo.")

                return paciente_id

            # Novo cadastro
            cursor.execute('''
                INSERT INTO pacientes (nome, cpf, telefone, email, data_nascimento, sexo, tipo_sanguineo, endereco, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ativo')
            ''', (nome, cpf, telefone, email, data_nascimento, sexo,
                  tipo_sanguineo, endereco))

            cursor.execute('''
                SELECT id FROM pacientes where cpf = ?
            ''', (cpf,))
            id = cursor.fetchone()[0]

            cursor.execute('''
                INSERT INTO triagens (paciente_id, escala_dor, escala_glascow, sinais_vitais) 
                VALUES (?, ?, ?, ?)
            ''', (id, escala_dor, escala_glascow, sinais_vitais))

            conn.commit()
            novo_id = cursor.lastrowid
            print(f"Novo paciente criado com ID {novo_id}.")

            if not self.verificar_triagem_vermelha(novo_id, escala_dor,
                                                   escala_glascow, sinais_vitais):
                # Adiciona à fila se não for caso vermelho
                if self.gerenciadorFila:
                    try:
                        self.gerenciadorFila.adicionar_paciente_fila(id_paciente=novo_id, tipo_fila=0, prioridade=3)
                        print("Paciente adicionado à fila.")
                    except Exception as e:
                        print(f"Erro ao adicionar novo paciente à fila: {e}")
    
            return novo_id
        
    def finalizar_ultimo_atendimento(self, paciente_id: int):
        """Finaliza o atendimento mais recente de um paciente."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM historico_atendimentos
                WHERE paciente_id = ?
                ORDER BY data DESC
                LIMIT 1
            ''', (paciente_id,))
            atendimento = cursor.fetchone()

            if atendimento:
                atendimento_id = atendimento[0]
                cursor.execute('''
                    UPDATE historico_atendimentos
                    SET status = 'finalizado'
                    WHERE id = ?
                ''', (atendimento_id,))
                conn.commit()
                print(f"Atendimento {atendimento_id} finalizado com sucesso.")
            else:
                print("Nenhum atendimento encontrado para finalizar.")

    def registrar_atendimento(self, paciente_id: int, sintomas: str, descricao: str, diagnostico: str,
                              status: str = "pendente", usuario_id: Optional[int] = None):
        """
        Registra um novo atendimento e atualiza a fila do paciente.

        Args:
            paciente_id: ID do paciente
            sintomas: sintomas relatados
            descricao: descrição do caso
            diagnostico: diagnóstico médico
            status: status do atendimento
            usuario_id: ID do profissional de saúde (opcional)
        """
        if not diagnostico or diagnostico.strip() == "":
            print("Diagnóstico não pode estar vazio.")
            return

        if not self.paciente_existe(paciente_id):
            print(f"Erro: paciente com ID {paciente_id} não existe.")
            return

        with self._conectar() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO historico_atendimentos (paciente_id, usuario_id, data, sintomas, descricao, diagnostico, status)
                    VALUES (?, ?, datetime('now'), ?, ?, ?, ?)
                ''', (paciente_id, usuario_id, sintomas, descricao, diagnostico, status))

                # Remove da fila atual e coloca na de atendidos
                cursor.execute('''DELETE FROM fila WHERE id_paciente = ?''', (paciente_id,))
                cursor.execute('''INSERT INTO fila (id_paciente, tipo_fila) VALUES (?, ?)''', (paciente_id, 1))
                conn.commit()
                print("Atendimento registrado com sucesso!")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao registrar atendimento: {e}")

    def obter_historico_paciente(self, paciente_id: int) -> List[Dict[str, Any]]:
        """Retorna o histórico de atendimentos do paciente, ordenado da data mais recente para a mais antiga."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT data, sintomas, descricao, diagnostico, status
                FROM historico_atendimentos
                WHERE paciente_id = ?
                ORDER BY data DESC
            ''', (paciente_id,))
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, row)) for row in cursor.fetchall()]

    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Consulta os pacientes com base nos filtros fornecidos."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM pacientes'
            params = []

            if filtros:
                clausulas = []
                for coluna, valor in filtros.items():
                    clausulas.append(f"{coluna} = ?")
                    params.append(valor)
                query += " WHERE " + " AND ".join(clausulas)

            cursor.execute(query, params)
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, row)) for row in cursor.fetchall()]

    def atualizar(self, id_paciente: int, novos_dados: Dict[str, Any]):
        """Atualiza informações do paciente com base no ID e campos passados."""
        if not novos_dados:
            print("Nenhum dado para atualizar.")
            return

        with self._conectar() as conn:
            cursor = conn.cursor()
            campos = ', '.join([f"{k} = ?" for k in novos_dados])
            valores = list(novos_dados.values()) + [id_paciente]
            cursor.execute(f'''
                UPDATE pacientes
                SET {campos}
                WHERE id = ?
            ''', valores)
            conn.commit()

    def remover(self, id_paciente: int):
        """Remove completamente o paciente do sistema."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
            conn.commit()

    def encerrar_atendimento(self, id_paciente: int):
        """Marca o paciente como desativo após atendimento."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE pacientes
                SET status = 'desativo'
                WHERE id = ?
            ''', (id_paciente,))
            conn.commit()

    def get_paciente(self, id):
        """Retorna o objeto Paciente via builder, com base no ID do banco."""
        with (self._conectar() as conn):
            paciente_builder = PacienteBuilder()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT nome, cpf, telefone, email, data_nascimento,
                sexo, tipo_sanguineo, endereco WHERE id=?
            ''', (id,))
            nome, cpf, telefone, email, data_nascimento, sexo, \
                tipo_sanguineo, endereco = cursor.fetchone()
            return paciente_builder.set_nome(nome) \
                .set_cpf(cpf) \
                .set_contato_emg([telefone, email]) \
                .set_idade(data_nascimento) \
                .set_sexo(sexo) \
                .set_tipo_sang(tipo_sanguineo) \
                .build()

    def get_triagem(self, id):
        """Obtém a cor da pulseira do paciente baseado na triagem."""
        with (self._conectar() as conn):
            cursor = conn.cursor()
            cursor.execute('''
                SELECT escala_dor, escala_glascow, sinais_vitais
                FROM triagens WHERE paciente_id=?
            ''', (id,))
            escala_dor, escala_glascow, sinais_vitais = cursor.fetchone()
            triagem = Triagem(None, int(escala_dor), int(escala_glascow), int(sinais_vitais))
            triagem.definir_prioridade()
            return triagem.get_cor_pulseira()

    def limpar_triagens(self, paciente_id):
        """Remove os dados de triagem de um paciente."""
        with (self._conectar() as conn):
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM triagens WHERE paciente_id = ?
            ''', (paciente_id,))

    # retorna true se a triagem for vermelha E for possível por o paciente em
    # um leito
    def verificar_triagem_vermelha(self, paciente_id, escala_dor, escala_glascow, sinais_vitais):
        """
        Verifica se a triagem é vermelha e tenta alocar o paciente em um leito.

        Returns:
            bool: True se foi possível alocar, False caso contrário.
        """
        triagem = Triagem(None, int(escala_dor), int(escala_glascow), int(sinais_vitais))
        triagem.definir_prioridade()
        if triagem.get_cor_pulseira() == Triagem.VERMELHA:
            gerenciador_leitos = GerenciadorLeitos()

            todos_leitos = gerenciador_leitos.consultar()
            ocupados = {
                l["numero_leito"]
                for l in todos_leitos
                if not l["data_saida"] and l["numero_leito"] is not None
            }

            total_leitos = 8  # pode ser dinâmico
            numero_disponivel = None
            for i in range(1, total_leitos + 1):
                if i not in ocupados:
                    numero_disponivel = i
                    break

            if numero_disponivel is None:
                return False

            data_entrada = datetime.now()
            gerenciador_leitos.inserir(numero_disponivel, paciente_id, 1,
                                       data_entrada.strftime("%Y-%m-%d %H:%M:%S"),
                                       (data_entrada + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
            return True
        return False
