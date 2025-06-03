import sqlite3

def criar_tab_fila():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Criar tabela usuarios (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fila (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            id_profissional_encaminhou INTEGER,
            data_entrada TEXT,
            id_fila INTEGER
        )
    ''')
    # SE for 1, é fila triagem, se for 2 é fila atendimento
    # Criar tabela pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fila (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            id_profissional_encaminhou INTEGER,
            data_entrada TEXT,
            id_fila INTEGER,
            posicao INTEGER, 
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.executemany('''
        INSERT OR IGNORE INTO leitos (id_paciente, id_profissional_encaminhou, data_entrada, id_fila, posicao)
        VALUES (?, ?, ?, ?)
    ''')
 
    conn.commit()
    conn.close()

    print("Tabela 'fila' criada e populada com dados padrões.")

# Executar
criar_tab_fila()
