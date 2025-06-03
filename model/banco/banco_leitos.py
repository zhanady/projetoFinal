import sqlite3

def criar_tab_leitos():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Criar tabela usuarios (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            id_medico_encaminhou INTEGER,
            data_entrada TEXT,
            data_saida TEXT
        )
    ''')

    # Criar tabela pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            id_medico_encaminhou INTEGER,
            data_entrada TEXT,
            data_saida TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.executemany('''
        INSERT OR IGNORE INTO leitos (id_paciente, id_medico_encaminhou, data_entrada, data_saida)
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
    

    conn.commit()
    conn.close()

    print("Tabela 'leitos' criada e populada com dados padrões.")

# Executar
criar_tab_leitos()
