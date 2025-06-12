import sqlite3
import json

class GerenciadorMensagens:
    def __init__(self, db_name='hospital.db'):
        """Inicializa a classe e cria a tabela se não existir"""
        self.db_name = db_name
        self._criar_tabela()
    
    def _conectar(self):
        """Cria e retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def _criar_tabela(self):
        """Cria a tabela de registros se não existir"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mensagem TEXT NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def inserir_mensagem(self, mensagem_dict):
        """
        Insere uma nova mensagem no banco de dados
        
        Args:
            mensagem_dict (dict): Dicionário com os dados da mensagem
        
        Returns:
            int: ID da mensagem inserida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Converter o dicionário para JSON
            mensagem_json = json.dumps(mensagem_dict)
            
            # Inserir no banco de dados
            cursor.execute('''
                INSERT INTO registros (mensagem)
                VALUES (?)
            ''', (mensagem_json,))
            
            conn.commit()
            return cursor.lastrowid
    
    def buscar_mensagens(self, filtros=None):
        """
        Busca mensagens com base em filtros opcionais
        
        Args:
            filtros (dict, optional): Dicionário com filtros de busca. Ex:
                {'id': 1} ou {'data_criacao': '2023-01-01'}
        
        Returns:
            list: Lista de dicionários com as mensagens encontradas
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT id, mensagem, data_criacao FROM registros'
            params = []
            
            if filtros:
                conditions = []
                for key, value in filtros.items():
                    if key == 'id':
                        conditions.append('id = ?')
                        params.append(value)
                    elif key == 'data_criacao':
                        conditions.append('date(data_criacao) = ?')
                        params.append(value)
                    # Adicione mais filtros conforme necessário
                
                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY data_criacao DESC'
            cursor.execute(query, params)
            
            # Converter resultados para dicionários
            resultados = []
            for linha in cursor.fetchall():
                resultado = dict(linha)
                # Converter mensagem JSON para dicionário
                resultado['mensagem'] = json.loads(resultado['mensagem'])
                resultados.append(resultado)
            
            return resultados
    
    def atualizar_mensagem(self, mensagem_id, nova_mensagem_dict):
        """
        Atualiza uma mensagem existente
        
        Args:
            mensagem_id (int): ID da mensagem a ser atualizada
            nova_mensagem_dict (dict): Novo conteúdo da mensagem
        
        Returns:
            bool: True se a atualização foi bem sucedida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            try:
                # Converter o novo dicionário para JSON
                nova_mensagem_json = json.dumps(nova_mensagem_dict)
                
                cursor.execute('''
                    UPDATE registros
                    SET mensagem = ?
                    WHERE id = ?
                ''', (nova_mensagem_json, mensagem_id))
                
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                conn.rollback()
                print(f"Erro ao atualizar mensagem: {e}")
                return False
    
    def remover_mensagem(self, mensagem_id):
        """
        Remove uma mensagem do banco de dados
        
        Args:
            mensagem_id (int): ID da mensagem a ser removida
        
        Returns:
            bool: True se a remoção foi bem sucedida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    DELETE FROM registros
                    WHERE id = ?
                ''', (mensagem_id,))
                
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                conn.rollback()
                print(f"Erro ao remover mensagem: {e}")
                return False

# Exemplo de uso
if __name__ == "__main__":
    gerenciador = GerenciadorMensagens()
    
    # Inserir mensagem de exemplo
    mensagem_id = gerenciador.inserir_mensagem({
        'hora': '10:30',
        'mensagem': 'Consulta marcada para o dia 15/05',
        'tipo': 'lembrete'
    })
    print(f"Mensagem inserida com ID: {mensagem_id}")
    
    # Buscar todas as mensagens
    mensagens = gerenciador.buscar_mensagens()
    print("\nTodas as mensagens:")
    for msg in mensagens:
        print(msg)
    
    # Buscar mensagem específica
    msg_especifica = gerenciador.buscar_mensagens({'id': mensagem_id})
    print(f"\nMensagem específica: {msg_especifica}")