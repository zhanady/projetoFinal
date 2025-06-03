import sqlite3

def criar_tab_usuarios():
    # Conecta (ou cria) o banco de dados
    conexao = sqlite3.connect('hospital.db')
    cursor = conexao.cursor()

    # Cria a tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            idade INTEGER,
            genero TEXT
        )
    ''')

    # Insere os dados padrões
    try:
        cursor.executemany('''
            INSERT INTO usuarios (nome, email, senha, idade, genero)
            VALUES (?, ?, ?, ?, ?)
        ''')
    except sqlite3.IntegrityError:
        print("Alguns dados já existem no banco e foram ignorados.")

    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()

    print("Banco de dados criado e populado com dados padrões!")

# 🔧 Executa a função
criar_tab_usuarios()
