import sqlite3

class GerenciadorProfissionais:
    def __init__(self, db_name='hospital.db'):
        """Inicializa a classe e cria as tabelas necessárias"""
        self.db_name = db_name
        self._criar_tabelas()
    
    def _conectar(self):
        """Cria e retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def _criar_tabelas(self):  # Corrigido o nome do método (tinha um typo)
        """Cria as tabelas de usuários e profissionais se não existirem"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários (dados comuns)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL, 
                    telefone TEXT,
                    email TEXT
                )
            ''')
            
            # Tabela de profissionais (dados específicos)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profissionais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    cargo TEXT NOT NULL,
                    departamento TEXT NOT NULL,
                    registro TEXT,
                    status TEXT NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
            conn.commit()
    
    def inserir_profissional(self, dados_usuario, dados_profissional):
        """
        Insere um novo profissional no banco de dados
        
        Args:
            dados_usuario (dict): Dados do usuário (nome, cpf, telefone, email)
            dados_profissional (dict): Dados do profissional (cargo, departamento, registro, status)
        
        Returns:
            int: ID do profissional inserido
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Inserir usuário
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios (nome, cpf, telefone, email)
                VALUES (:nome, :cpf, :telefone, :email)
            ''', dados_usuario)
            
            # Obter ID do usuário
            usuario_id = cursor.lastrowid
            if usuario_id == 0:  # Se o usuário já existia
                cursor.execute('SELECT id FROM usuarios WHERE cpf = ?', (dados_usuario['cpf'],))
                usuario_id = cursor.fetchone()[0]
            
            # Inserir profissional
            dados_profissional['usuario_id'] = usuario_id
            cursor.execute('''
                INSERT INTO profissionais (usuario_id, cargo, departamento, registro, status)
                VALUES (:usuario_id, :cargo, :departamento, :registro, :status)
            ''', dados_profissional)
            
            conn.commit()
            return cursor.lastrowid


    def buscar_profissionais(self, filtros=None):
        """
        Busca profissionais com base em filtros opcionais
        
        Args:
            filtros (dict, optional): Dicionário com filtros de busca. Ex:
                {'cargo': 'Médico', 'status': 'Ativo'}
        
        Returns:
            list: Lista de dicionários com os profissionais encontrados
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row  # Para retornar dicionários
            cursor = conn.cursor()
            
            query = '''
                SELECT u.id as usuario_id, u.nome, u.cpf, u.telefone, u.email,
                       p.id as profissional_id, p.cargo, p.departamento, 
                       p.registro, p.status
                FROM usuarios u
                JOIN profissionais p ON u.id = p.usuario_id
            '''
            
            params = []
            if filtros:
                conditions = []
                for key, value in filtros.items():
                    if key in ['cargo', 'departamento', 'status', 'registro']:
                        conditions.append(f"p.{key} = ?")
                        params.append(value)
                    elif key in ['nome', 'cpf', 'telefone', 'email']:
                        conditions.append(f"u.{key} LIKE ?")
                        params.append(f"%{value}%")
                    elif key == 'id':
                        conditions.append("p.id = ?")
                        params.append(value)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def atualizar_profissional(self, profissional_id, dados_profissional, dados_usuario=None):
        """
        Atualiza os dados de um profissional
        
        Args:
            profissional_id (int): ID do profissional a ser atualizado
            dados_profissional (dict): Dados do profissional para atualizar
            dados_usuario (dict, optional): Dados do usuário para atualizar
        
        Returns:
            bool: True se a atualização foi bem sucedida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            try:
                # Atualizar dados do profissional
                if dados_profissional:
                    set_clause = ", ".join([f"{key} = ?" for key in dados_profissional.keys()])
                    values = list(dados_profissional.values())
                    values.append(profissional_id)
                    
                    cursor.execute(f'''
                        UPDATE profissionais
                        SET {set_clause}
                        WHERE id = ?
                    ''', values)
                
                # Atualizar dados do usuário se fornecidos
                if dados_usuario:
                    # Primeiro precisamos obter o usuario_id
                    cursor.execute('''
                        SELECT usuario_id FROM profissionais WHERE id = ?
                    ''', (profissional_id,))
                    usuario_id = cursor.fetchone()[0]
                    
                    set_clause = ", ".join([f"{key} = ?" for key in dados_usuario.keys()])
                    values = list(dados_usuario.values())
                    values.append(usuario_id)
                    
                    cursor.execute(f'''
                        UPDATE usuarios
                        SET {set_clause}
                        WHERE id = ?
                    ''', values)
                
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"Erro ao atualizar profissional: {e}")
                return False

    def remover_profissional(self, profissional_id):
        """
        Remove um profissional do sistema (remove o usuário associado também)
        
        Args:
            profissional_id (int): ID do profissional a ser removido
        
        Returns:
            bool: True se a remoção foi bem sucedida
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            try:
                # Primeiro obtemos o usuario_id
                cursor.execute('''
                    SELECT usuario_id FROM profissionais WHERE id = ?
                ''', (profissional_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False
                
                usuario_id = result[0]
                
                # Remover o profissional
                cursor.execute('''
                    DELETE FROM profissionais WHERE id = ?
                ''', (profissional_id,))
                
                # Remover o usuário associado
                cursor.execute('''
                    DELETE FROM usuarios WHERE id = ?
                ''', (usuario_id,))
                
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"Erro ao remover profissional: {e}")
                return False

    def inserir_dados_exemplo(self):
        """Insere dados de exemplo para teste"""
        exemplos = [
            (
                {'nome': 'Ana Silva', 'cpf': '12345678900', 
                 'telefone': '11999998888', 'email': 'ana@email.com'},
                {'cargo': 'Médica', 'departamento': 'Emergência', 
                 'registro': 'CRM12345', 'status': 'Ativo'}
            ),
            (
                {'nome': 'Carlos Oliveira', 'cpf': '98765432100', 
                 'telefone': '21988887777', 'email': 'carlos@email.com'},
                {'cargo': 'Enfermeiro', 'departamento': 'UTI', 
                 'registro': 'COREN54321', 'status': 'Ativo'}
            ),
            (
                {'nome': 'Juliana Costa', 'cpf': '45678912300', 
                 'telefone': '31977776666', 'email': 'juliana@email.com'},
                {'cargo': 'Técnico de Enfermagem', 'departamento': 'Clínica', 
                 'registro': 'COREN67890', 'status': 'Licença'}
            )
        ]
        
        for usuario, profissional in exemplos:
            self.inserir_profissional(usuario, profissional)