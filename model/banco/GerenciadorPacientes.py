import sqlite3
from typing import Optional, Dict, Any, List
from projetoFinal.model.banco.GerenciadorFila import *

class GerenciadorPacientes:
    def __init__(self, db_name: str = '../hospital.db'):
        self.db_name = db_name
        self._criar_tabelas()
        self.gerenciadorFila = GerenciadorFila()


    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabelas(self):
        """
            Cria as tabelas necessárias para o funcionamento da lógica dos pacientes:
            primeiro cria a tabela de triagem, depois a tabela de pacientes e por fim
            a tabela de histórico
        """
        with self._conectar() as conn:
            cursor = conn.cursor()


            cursor.execute('''
                CREATE TABLE IF NOT EXISTS triagem (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    escala_dor INTEGER NOT NULL,
                    escala_glascow INTEGER NOT NULL
                    sinais_vitais INTEGER NOT NULL
                );
            ''')

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
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM pacientes WHERE id = ?", (id_paciente,))
            return cursor.fetchone() is not None

    def cadastrar_ou_reativar(self, nome, cpf, telefone, email, data_nascimento, sexo, tipo_sanguineo, endereco):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, status FROM pacientes WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()

            if resultado:
                paciente_id, status_atual = resultado
                # Se já existe e está inativo, reativar
                if status_atual.lower() == "inativo":
                    cursor.execute("UPDATE pacientes SET status = 'ativo' WHERE id = ?", (paciente_id,))
                    conn.commit()
                    print(f"Paciente com CPF {cpf} reativado.")
                    self.gerenciadorFila.adicionar_paciente_fila(id_paciente=paciente_id, tipo_fila=0, prioridade=3)

                else:
                    print(f"Paciente com CPF {cpf} já está ativo.")
                    #self.gerenciadorFila.adicionar_paciente_fila(id_paciente=paciente_id, tipo_fila=0, prioridade=3)

                return paciente_id

            # Caso não exista, criar novo
            cursor.execute('''
                INSERT INTO pacientes (nome, cpf, telefone, email, data_nascimento, sexo, tipo_sanguineo, endereco, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ativo')
            ''', (nome, cpf, telefone, email, data_nascimento, sexo, tipo_sanguineo, endereco))
            conn.commit()
            novo_id = cursor.lastrowid
            print(f"Novo paciente criado com ID {novo_id}.")
            return novo_id


        # Verifica se o paciente de fato está no banco
        teste = self.consultar(filtros={"id": id_paciente})
        print("Consulta paciente por ID:", teste)
        # Agora fora do `with` (ou use novo `with`), para evitar reuso de conexão antiga
        if self.gerenciadorFila and id_paciente:
            try:
                self.gerenciadorFila.adicionar_paciente_fila(id_paciente=id_paciente, tipo_fila=0, prioridade=3)
            except Exception as e:
                print(f"Erro ao adicionar paciente à fila: {e}")
                return None

        return id_paciente
    def finalizar_ultimo_atendimento(self, paciente_id: int):
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

    def registrar_atendimento(self, paciente_id: int, sintomas: str, descricao: str, diagnostico: str, status: str = "pendente", usuario_id: Optional[int] = None):
        if not diagnostico or diagnostico.strip() == "":
            print("Diagnóstico não pode estar vazio.")
            return

        # Verificar se o paciente existe antes de inserir
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
                conn.commit()
                print("Atendimento registrado com sucesso!")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao registrar atendimento: {e}")

    def obter_historico_paciente(self, paciente_id: int) -> List[Dict[str, Any]]:
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
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
            conn.commit()

    def encerrar_atendimento(self, id_paciente: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE pacientes
                SET status = 'desativo'
                WHERE id = ?
            ''', (id_paciente,))
            conn.commit()
