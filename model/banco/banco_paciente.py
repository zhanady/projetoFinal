import sqlite3

def criar_tab_pacientes():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Criar tabela usuarios (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT
        )
    ''')

    # Criar tabela pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data_nascimento TEXT,
            sexo TEXT,
            tipo_sanguineo TEXT,
            endereco TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.executemany('''
        INSERT OR IGNORE INTO usuarios (nome, cpf, telefone, email)
        VALUES (?, ?, ?, ?)
    ''')

    # Obter IDs dos usuários
    ''''    
        cursor.execute("SELECT id FROM usuarios WHERE cpf = '11122233344'")
        marcos_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM usuarios WHERE cpf = '55566677788'")
        lucia_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM usuarios WHERE cpf = '99988877766'")
        pedro_id = cursor.fetchone()[0]
    '''
    cursor.executemany('''
        INSERT OR IGNORE INTO pacientes (usuario_id, data_nascimento, sexo, tipo_sanguineo, endereco, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''')

    conn.commit()
    conn.close()

    print("Tabela 'pacientes' criada e populada com dados padrões.")

# Executar
criar_tab_pacientes()
