import sqlite3

def criar_tab_profissional():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Criar tabela de usuários (dados comuns)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT
        )
    ''')

    # Criar tabela de profissionais (dados específicos)
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

    cursor.executemany('''
        INSERT OR IGNORE INTO usuarios (nome, cpf, telefone, email)
        VALUES (?, ?, ?, ?)
    ''')
    '''
        # Buscar IDs dos usuários
        cursor.execute("SELECT id FROM usuarios WHERE cpf = '12345678900'")
        ana_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM usuarios WHERE cpf = '98765432100'")
        carlos_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM usuarios WHERE cpf = '45678912300'")
        juliana_id = cursor.fetchone()[0]
    '''
    '''
        # Inserir profissionais vinculados aos usuários
        profissionais = [
            (ana_id, 'Médica', 'Emergência', 'CRM12345', 'Ativo'),
            (carlos_id, 'Enfermeiro', 'UTI', 'COREN54321', 'Ativo'),
            (juliana_id, 'Técnico de Enfermagem', 'Clínica', 'COREN67890', 'Licença'),
        ]
    '''    
    cursor.executemany('''
        INSERT OR IGNORE INTO profissionais (usuario_id, cargo, departamento, registro, status)
        VALUES (?, ?, ?, ?, ?)
    ''')

    conn.commit()
    conn.close()

    print("Banco de dados criado com tabelas 'usuarios' e 'profissionais' relacionadas.")

# Executar
criar_tab_profissional()
