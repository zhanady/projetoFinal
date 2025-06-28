import sqlite3
from datetime import datetime

class GerenciadorFila:
    def __init__(self, db_name='hospital.db'):
        """Inicializa a classe e cria as tabelas necessárias"""
        self.db_name = db_name
        self._criar_tabelas()
    
    def _conectar(self):
        """Cria e retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def _criar_tabelas(self):
        """Cria as tabelas relacionadas à fila hospitalar"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela principal da fila
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fila (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_paciente INTEGER NOT NULL,
                    id_profissional_encaminhou INTEGER,
                    data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tipo_fila INTEGER NOT NULL,  -- 1: Triagem, 2: Atendimento
                    status TEXT DEFAULT 'Pendente',  -- Pendente, Em Atendimento, Finalizado
                    prioridade INTEGER DEFAULT 3,  -- 1: Alta, 2: Média, 3: Baixa
                    FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
                    FOREIGN KEY (id_profissional_encaminhou) REFERENCES profissionais(id)
                )
            ''')

            # Tabela de profissionais (necessária para os joins)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profissionais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    especialidade TEXT,
                    registro TEXT
                )
            ''')

            
            # Tabela de histórico de movimentação na fila
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fila_historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_fila INTEGER NOT NULL,
                    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status_anterior TEXT,
                    status_novo TEXT,
                    observacoes TEXT,
                    FOREIGN KEY (id_fila) REFERENCES fila(id)
                )
            ''')
            
            conn.commit()
    
    def adicionar_paciente_fila(self, id_paciente, tipo_fila, id_profissional=None, prioridade=3):
        """
        Adiciona um paciente à fila
        
        Args:
            id_paciente (int): ID do paciente
            tipo_fila (int): 1 para Triagem, 2 para Atendimento
            id_profissional (int, optional): ID do profissional que encaminhou
            prioridade (int): 1 (Alta), 2 (Média), 3 (Baixa)
        
        Returns:
            int: ID do registro na fila
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO fila (id_paciente, id_profissional_encaminhou, tipo_fila, prioridade)
                VALUES (?, ?, ?, ?)
            ''', (id_paciente, id_profissional, tipo_fila, prioridade))
            
            id_fila = cursor.lastrowid
            
            # Registrar no histórico
            cursor.execute('''
                INSERT INTO fila_historico (id_fila, status_anterior, status_novo)
                VALUES (?, 'Novo', 'Pendente')
            ''', (id_fila,))
            
            conn.commit()
            return id_fila
    
    def atualizar_status_fila(self, id_fila, novo_status, observacoes=None):
        """
        Atualiza o status de um paciente na fila
        
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
                # Obter status atual
                cursor.execute('SELECT status FROM fila WHERE id = ?', (id_fila,))
                status_atual = cursor.fetchone()[0]
                
                # Atualizar fila principal
                cursor.execute('''
                    UPDATE fila
                    SET status = ?
                    WHERE id = ?
                ''', (novo_status, id_fila))
                
                # Registrar no histórico
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
        Busca pacientes na fila com filtros opcionais
        
        Args:
            tipo_fila (int, optional): 1 (Triagem) ou 2 (Atendimento)
            status (str, optional): Status para filtrar
            prioridade (int, optional): Prioridade para filtrar (1-3)
        
        Returns:
            list: Lista de dicionários com os registros da fila
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT f.id, f.id_paciente, f.id_profissional_encaminhou, 
                       f.data_entrada, f.tipo_fila, f.status, f.prioridade,
                       p.nome as nome_paciente, pr.nome as nome_profissional
                FROM fila f
                LEFT JOIN pacientes p ON f.id_paciente = p.id
                LEFT JOIN profissionais pr ON f.id_profissional_encaminhou = pr.id
            '''
            
            conditions = []
            params = []
            
            if tipo_fila:
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
        Busca o histórico de movimentações de um paciente na fila
        
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
    
    # Adicionar paciente à fila de triagem
    id_fila = gerenciador.adicionar_paciente_fila(
        id_paciente=1,
        tipo_fila=1,
        id_profissional=3,
        prioridade=2
    )
    print(f"Paciente adicionado à fila com ID: {id_fila}")
    
    # Buscar fila de triagem
    fila_triagem = gerenciador.buscar_fila(tipo_fila=1)
    print("\nFila de Triagem:")
    for paciente in fila_triagem:
        print(paciente)
    
    # Atualizar status
    gerenciador.atualizar_status_fila(
        id_fila=id_fila,
        novo_status="Em Atendimento",
        observacoes="Iniciado atendimento de triagem"
    )
    
    # Ver histórico
    historico = gerenciador.buscar_historico_fila(id_fila)
    print("\nHistórico do paciente:")
    for registro in historico:
        print(registro)