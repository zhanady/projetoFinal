import sqlite3

class GerenciadorFarmacia:
    def __init__(self, db_name='../hospital.db'):
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
            
            # Criação da tabela "farmacia" com campos principais para controle de medicamentos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS farmacia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,                    -- Identificador único
                    medicamento TEXT NOT NULL,                               -- Nome do medicamento
                    principio_ativo TEXT NOT NULL,                           -- Princípio ativo
                    concentracao TEXT NOT NULL,                              -- Dosagem/concentração
                    quantidade INTEGER NOT NULL DEFAULT 0,                   -- Quantidade em estoque
                    unidade_medida TEXT NOT NULL,                            -- Unidade (comprimidos, frascos, etc)
                    lote TEXT,                                               -- Lote (opcional)
                    data_validade TEXT,                                      -- Data de validade (opcional)
                    categoria TEXT,                                          -- Categoria do medicamento (opcional)
                    minimo_estoque INTEGER DEFAULT 10,                       -- Estoque mínimo permitido
                    maximo_estoque INTEGER DEFAULT 100,                      -- Estoque máximo recomendado
                    fornecedor TEXT,                                         -- Fornecedor do medicamento
                    codigo_barras TEXT UNIQUE,                               -- Código de barras (único, se houver)
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP        -- Data de cadastro automática
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
            
            # Verificar se já existem registros na tabela
            cursor.execute('SELECT COUNT(*) FROM farmacia')
            if cursor.fetchone()[0] == 0:
                # Inserir dados básicos se a tabela estiver vazia
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
            
            campos = []        # Lista de campos a serem inseridos
            valores = []       # Lista de valores correspondentes
            placeholders = []  # Lista de "?" para uso seguro no SQL
            
            for campo, valor in medicamento_data.items():
                campos.append(campo)
                valores.append(valor)
                placeholders.append('?')
            
            # Montagem da query de inserção dinâmica com base nos dados fornecidos
            query = f'''
                INSERT INTO farmacia ({', '.join(campos)})
                VALUES ({', '.join(placeholders)})
            '''
            
            cursor.execute(query, valores)
            conn.commit()
            return cursor.lastrowid  # Retorna o ID do novo registro inserido
    
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
                # Atualiza a coluna "quantidade" para o medicamento especificado
                cursor.execute('''
                    UPDATE farmacia
                    SET quantidade = ?
                    WHERE id = ?
                ''', (nova_quantidade, medicamento_id))
                
                conn.commit()
                return cursor.rowcount > 0  # Retorna True se algum registro foi alterado
            except Exception as e:
                conn.rollback()  # Desfaz qualquer alteração no caso de erro
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
            conn.row_factory = sqlite3.Row  # Permite retornar resultados como dicionários
            cursor = conn.cursor()
            
            query = 'SELECT * FROM farmacia'
            conditions = []  # Lista de condições WHERE
            params = []      # Lista de parâmetros para passar na query
            
            if filtros:
                for campo, valor in filtros.items():
                    if campo.endswith('_min'):
                        # Campo mínimo (ex: quantidade_min)
                        campo_real = campo.replace('_min', '')
                        conditions.append(f"{campo_real} >= ?")
                        params.append(valor)
                    elif campo.endswith('_max'):
                        # Campo máximo (ex: quantidade_max)
                        campo_real = campo.replace('_max', '')
                        conditions.append(f"{campo_real} <= ?")
                        params.append(valor)
                    elif campo == 'busca':
                        # Filtro por texto no nome do medicamento ou princípio ativo
                        conditions.append('(medicamento LIKE ? OR principio_ativo LIKE ?)')
                        params.extend([f"%{valor}%", f"%{valor}%"])
                    else:
                        # Igualdade direta
                        conditions.append(f"{campo} = ?")
                        params.append(valor)
                
                if conditions:
                    # Adiciona a cláusula WHERE com as condições montadas
                    query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY medicamento'  # Ordena por nome do medicamento
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]  # Retorna como lista de dicionários
    
    def verificar_estoque_baixo(self):
        """
        Retorna medicamentos com estoque abaixo do mínimo
        
        Returns:
            list: Lista de medicamentos com estoque baixo
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Seleciona todos os medicamentos com quantidade menor que o mínimo permitido
            cursor.execute('''
                SELECT * FROM farmacia
                WHERE quantidade < minimo_estoque
                ORDER BY quantidade ASC
            ''')
            
            return [dict(row) for row in cursor.fetchall()]  # Retorna resultados formatados

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
