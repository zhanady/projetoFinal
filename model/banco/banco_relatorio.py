import sqlite3

def criar_tabela_relatorio():
    # Conectar ao banco de dados (cria se não existir)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Criar tabela 'relatorio' se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_total REAL,
            observacao TEXT
        )
    ''')

    # Inserir os dados
    cursor.executemany('''
        INSERT INTO relatorio (data, categoria, quantidade, valor_total, observacao)
        VALUES (?, ?, ?, ?, ?)
    ''')

    conn.commit()
    conn.close()

    print("Tabela 'relatorio' criada e populada com dados estatísticos!")


# 🔧 Executar a função
criar_tabela_relatorio()
