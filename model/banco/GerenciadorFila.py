import sqlite3
from datetime import datetime

class GerenciadorFila:
    def __init__(self, db_name='../hospital.db'):
        """Inicializa a classe e cria as tabelas necessárias"""
        self.db_name = db_name
        self._criar_tabelas()
    
    def _conectar(self):
        # Cria e retorna uma conexão com o banco de dados, ativando chaves estrangeiras
        conn = sqlite3.connect(self.db_name)
        return conn

    def _criar_tabelas(self):
        """Cria as tabelas relacionadas à fila hospitalar"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela principal de controle da fila
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS fila (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_fila INTEGER NOT NULL,
                status TEXT DEFAULT 'Pendente',
                prioridade INTEGER DEFAULT 3
            )
        ''')

            # Tabela de profissionais (referenciada na fila)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profissionais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    especialidade TEXT,
                    registro TEXT
                );
            ''')

            # Tabela de histórico de movimentações da fila
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fila_historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_fila INTEGER NOT NULL,
                    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status_anterior TEXT,
                    status_novo TEXT,
                    observacoes TEXT
                );
            ''')

            conn.commit()

    def dar_alta(self):
        """
        Remove o paciente da fila de atendimento (tipo 1),
        usado ao concluir o atendimento médico.
        """
        try:
            self.gerenciador_fila.remover_paciente_fila(self.paciente["id"], tipo_fila=1)
            print("Paciente removido da fila de atendimento.")
            self.mostrar_fila()
        except Exception as e:
            print(f"Erro ao dar alta: {e}")

    def remover_paciente_fila(self, id_paciente: int, tipo_fila: int):
        """
        Remove um paciente da fila especificada.
        
        Args:
            id_paciente (int): ID do paciente
            tipo_fila (int): Tipo da fila (0: Triagem, 1: Atendimento)
        """
        with self._conectar() as conn:
            cursor = conn.cursor()

            # Busca o primeiro registro da fila para esse paciente e tipo
            cursor.execute('''
                SELECT id FROM fila
                WHERE id_paciente = ? AND tipo_fila = ?
                ORDER BY data_entrada ASC
            ''', (id_paciente, tipo_fila))
            resultado = cursor.fetchone()

            if resultado:
                id_fila = resultado[0]

                # Registra a movimentação como removido no histórico
                cursor.execute('''
                    INSERT INTO fila_historico (id_fila, status_anterior, status_novo, observacoes)
                    VALUES (?, 'Pendente', 'Removido', 'Removido automaticamente ao progredir de fila.')
                ''', (id_fila,))

                # Remove da fila principal
                cursor.execute('DELETE FROM fila WHERE id = ?', (id_fila,))
                conn.commit()
            else:
                print(f"Nenhum registro encontrado na fila {tipo_fila} para o paciente {id_paciente}.")

    def adicionar_paciente_fila(self, id_paciente, tipo_fila, prioridade=3):
        """
        Adiciona um paciente à fila de triagem (0) ou atendimento (1).
        
        Args:
            id_paciente (int): ID do paciente
            tipo_fila (int): 0 = Triagem, 1 = Atendimento
            id_profissional (int): ID do profissional que encaminhou (opcional)
            prioridade (int): Prioridade (1: Alta, 2: Média, 3: Baixa)
        
        Returns:
            int: ID da entrada na fila
        """
        with self._conectar() as conn:
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO fila (id_paciente, tipo_fila, prioridade)
            VALUES (?, ?, ?)
        ''', (id_paciente, tipo_fila, prioridade))



            id_fila = cursor.lastrowid

            # Inserir entrada no histórico com status inicial
            cursor.execute('''
                INSERT INTO fila_historico (id_fila, status_anterior, status_novo)
                VALUES (?, 'Novo', 'Pendente')
            ''', (id_fila,))

            conn.commit()
            return id_fila

    def atualizar_status_fila(self, id_fila, novo_status, observacoes=None):
        """
        Atualiza o status de um paciente na fila.
        
        Args:
            id_fila (int): ID do registro na fila
            novo_status (str): Novo status (Pendente, Em Atendimento, Finalizado)
            observacoes (str, optional): Observações sobre a mudança
        
        Returns:
            bool: True se a atualização foi bem sucedida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            try:
                # Recuperar o status atual
                cursor.execute('SELECT status FROM fila WHERE id = ?', (id_fila,))
                status_atual = cursor.fetchone()[0]
                
                # Atualizar o status
                cursor.execute('''
                    UPDATE fila
                    SET status = ?
                    WHERE id = ?
                ''', (novo_status, id_fila))
                
                # Registrar a movimentação no histórico
                cursor.execute('''
                    INSERT INTO fila_historico 
                    (id_fila, status_anterior, status_novo, observacoes)
                    VALUES (?, ?, ?, ?)
                ''', (id_fila, status_atual, novo_status, observacoes))
                
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"Erro ao atualizar status: {e}")
                return False

    def buscar_fila(self, tipo_fila=None, status=None, prioridade=None):
        """
        Busca pacientes na fila com filtros opcionais.
        
        Args:
            tipo_fila (int, optional): 0 (Triagem) ou 1 (Atendimento)
            status (str, optional): Filtrar por status atual
            prioridade (int, optional): Prioridade (1: Alta, 2: Média, 3: Baixa)
        
        Returns:
            list: Lista de dicionários com os registros da fila
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Consulta com JOINs para trazer nomes de paciente e profissional
            query = '''
                SELECT f.id, f.id_paciente,
                f.data_entrada, f.tipo_fila, f.status, f.prioridade,
                p.nome as nome_paciente
            FROM fila f
            LEFT JOIN pacientes p ON f.id_paciente = p.id

            '''

            conditions = []
            params = []

            # Aplica os filtros conforme os parâmetros
            if tipo_fila is not None:
                conditions.append('f.tipo_fila = ?')
                params.append(tipo_fila)

            if status:
                conditions.append('f.status = ?')
                params.append(status)

            if prioridade:
                conditions.append('f.prioridade = ?')
                params.append(prioridade)

            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)

            query += ' ORDER BY f.prioridade, f.data_entrada'

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def buscar_historico_fila(self, id_fila):
        """
        Busca o histórico de movimentações de um paciente na fila.
        
        Args:
            id_fila (int): ID do registro na fila
        
        Returns:
            list: Lista de dicionários com o histórico
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT data_movimentacao, status_anterior, status_novo, observacoes
                FROM fila_historico
                WHERE id_fila = ?
                ORDER BY data_movimentacao DESC
            ''', (id_fila,))

            return [dict(row) for row in cursor.fetchall()]


# Exemplo de uso
if __name__ == "__main__":
    gerenciador = GerenciadorFila()

    # Adiciona paciente à fila de triagem (tipo 0)
    id_fila = gerenciador.adicionar_paciente_fila(
        id_paciente=1,
        tipo_fila=0,  # Triagem
        #id_profissional=3,
        prioridade=2
    )
    print(f"Paciente adicionado à fila com ID: {id_fila}")

    # Buscar fila de triagem (tipo 0)
    fila_triagem = gerenciador.buscar_fila(tipo_fila=0)
    print("\nFila de Triagem:")
    for paciente in fila_triagem:
        print(paciente)

    # Atualizar status da fila para "Em Atendimento"
    gerenciador.atualizar_status_fila(
        id_fila=id_fila,
        novo_status="Em Atendimento",
        observacoes="Iniciado atendimento de triagem"
    )

    # Ver histórico de movimentações do paciente
    historico = gerenciador.buscar_historico_fila(id_fila)
    print("\nHistórico do paciente:")
    for registro in historico:
        print(registro)
