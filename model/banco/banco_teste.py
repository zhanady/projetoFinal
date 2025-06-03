import sqlite3

# Conectando ao banco de dados existente
conn = sqlite3.connect('teste.db')

# Executando um comando SQL para criar uma tabela
conn.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER)')

# Criar um cursor (permite executar comandos SQL)
cursor = conn.cursor()

# Conectar ao banco de dados
conn = sqlite3.connect('teste.db')
cursor = conn.cursor()

# Inserir um registro na tabela 'usuarios'
cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", ("Zainab", 18))

# Confirmar (salvar) as alterações
conn.commit()


# Executar SELECT para buscar todos os dados da tabela 'usuarios'
cursor.execute('SELECT * FROM usuarios')

# Buscar todos os resultados
resultado = cursor.fetchall()

# Exibir os resultados
for linha in resultado:
    print(linha)

# Fechar a conexão
conn.close()
