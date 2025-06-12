import sqlite3

class GerenciadorFarmacia:
    def __init__(self, db_name='hospital.db'):
        """Inicializa a classe e cria as tabelas necessárias"""
        self.db_name = db_name
        self._criar_tabelas()
        self._popular_dados_iniciais()
    
    def _conectar(self):
        """Cria e retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def _criar_tabelas(self):
        """Cria a tabela de farmácia se não existir"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS farmacia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    medicamento TEXT NOT NULL,
                    principio_ativo TEXT NOT NULL,
                    concentracao TEXT NOT NULL,
                    quantidade INTEGER NOT NULL DEFAULT 0,
                    unidade_medida TEXT NOT NULL,
                    lote TEXT,
                    data_validade TEXT,
                    categoria TEXT,
                    minimo_estoque INTEGER DEFAULT 10,
                    maximo_estoque INTEGER DEFAULT 100,
                    fornecedor TEXT,
                    codigo_barras TEXT UNIQUE,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def _popular_dados_iniciais(self):
        """Popula a tabela com medicamentos básicos se estiver vazia"""
        medicamentos_base = [
            ('Dipirona', 'Dipirona Sódica', '500mg', 100, 'comprimidos'),
            ('Paracetamol', 'Paracetamol', '750mg', 80, 'comprimidos'),
            ('Amoxicilina', 'Amoxicilina Triidratada', '500mg', 50, 'cápsulas'),
            ('Omeprazol', 'Omeprazol', '20mg', 120, 'cápsulas'),
            ('Losartana', 'Losartana Potássica', '50mg', 60, 'comprimidos')
        ]
        
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Verificar se a tabela está vazia
            cursor.execute('SELECT COUNT(*) FROM farmacia')
            if cursor.fetchone()[0] == 0:
                cursor.executemany('''
                    INSERT INTO farmacia 
                    (medicamento, principio_ativo, concentracao, quantidade, unidade_medida)
                    VALUES (?, ?, ?, ?, ?)
                ''', medicamentos_base)
                
                conn.commit()
    
    def adicionar_medicamento(self, medicamento_data):
        """
        Adiciona um novo medicamento ao estoque
        
        Args:
            medicamento_data (dict): Dados do medicamento contendo:
                - medicamento (str): Nome do medicamento
                - principio_ativo (str): Princípio ativo
                - concentracao (str): Concentração
                - quantidade (int): Quantidade em estoque
                - unidade_medida (str): Unidade de medida (comprimidos, frascos, etc)
                - outros campos opcionais
        
        Returns:
            int: ID do medicamento inserido
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            campos = []
            valores = []
            placeholders = []
            
            for campo, valor in medicamento_data.items():
                campos.append(campo)
                valores.append(valor)
                placeholders.append('?')
            
            query = f'''
                INSERT INTO farmacia ({', '.join(campos)})
                VALUES ({', '.join(placeholders)})
            '''
            
            cursor.execute(query, valores)
            conn.commit()
            return cursor.lastrowid
    
    def atualizar_estoque(self, medicamento_id, nova_quantidade):
        """
        Atualiza a quantidade em estoque de um medicamento
        
        Args:
            medicamento_id (int): ID do medicamento
            nova_quantidade (int): Nova quantidade em estoque
        
        Returns:
            bool: True se a atualização foi bem sucedida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    UPDATE farmacia
                    SET quantidade = ?
                    WHERE id = ?
                ''', (nova_quantidade, medicamento_id))
                
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                conn.rollback()
                print(f"Erro ao atualizar estoque: {e}")
                return False
    
    def buscar_medicamentos(self, filtros=None):
        """
        Busca medicamentos com base em filtros opcionais
        
        Args:
            filtros (dict, optional): Dicionário com filtros de busca. Ex:
                {'principio_ativo': 'Dipirona', 'quantidade_max': 50}
        
        Returns:
            list: Lista de dicionários com os medicamentos encontrados
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM farmacia'
            conditions = []
            params = []
            
            if filtros:
                for campo, valor in filtros.items():
                    if campo.endswith('_min'):
                        campo_real = campo.replace('_min', '')
                        conditions.append(f"{campo_real} >= ?")
                        params.append(valor)
                    elif campo.endswith('_max'):
                        campo_real = campo.replace('_max', '')
                        conditions.append(f"{campo_real} <= ?")
                        params.append(valor)
                    elif campo == 'busca':
                        conditions.append('(medicamento LIKE ? OR principio_ativo LIKE ?)')
                        params.extend([f"%{valor}%", f"%{valor}%"])
                    else:
                        conditions.append(f"{campo} = ?")
                        params.append(valor)
                
                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY medicamento'
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def verificar_estoque_baixo(self):
        """
        Retorna medicamentos com estoque abaixo do mínimo
        
        Returns:
            list: Lista de medicamentos com estoque baixo
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM farmacia
                WHERE quantidade < minimo_estoque
                ORDER BY quantidade ASC
            ''')
            
            return [dict(row) for row in cursor.fetchall()]

# Exemplo de uso
if __name__ == "__main__":
    farmacia = GerenciadorFarmacia()
    
    # Adicionar novo medicamento
    novo_med = farmacia.adicionar_medicamento({
        'medicamento': 'Ibuprofeno',
        'principio_ativo': 'Ibuprofeno',
        'concentracao': '400mg',
        'quantidade': 75,
        'unidade_medida': 'comprimidos',
        'data_validade': '2024-12-31'
    })
    print(f"Medicamento adicionado com ID: {novo_med}")
    
    # Buscar todos os medicamentos
    medicamentos = farmacia.buscar_medicamentos()
    print("\nTodos os medicamentos:")
    for med in medicamentos:
        print(f"{med['id']}: {med['medicamento']} - {med['quantidade']} {med['unidade_medida']}")
    
    # Buscar com filtros
    analgesicos = farmacia.buscar_medicamentos({
        'busca': 'Dipirona',
        'quantidade_min': 50
    })
    print("\nAnalgésicos encontrados:")
    for med in analgesicos:
        print(med['medicamento'])
    
    # Verificar estoque baixo
    estoque_baixo = farmacia.verificar_estoque_baixo()
    print("\nMedicamentos com estoque baixo:")
    for med in estoque_baixo:
        print(f"{med['medicamento']} - Estoque: {med['quantidade']} (Mínimo: {med['minimo_estoque']})")