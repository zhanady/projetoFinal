import sqlite3
import json

# Conectar ao banco de dados (será criado se não existir)
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Criar tabela para armazenar id e mensagem (como dicionário JSON)
cursor.execute('''
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mensagem TEXT NOT NULL
)
''')

#fazer receber os dados, coloquei aqi como exemplo
mensagem_dict = {
    'hora': "texto",
    'mensagem': 'texto'
}

# Converter o dicionário para JSON antes de inserir
mensagem_json = json.dumps(mensagem_dict)

# Inserir no banco de dados
cursor.execute('INSERT INTO registros (mensagem) VALUES (?)', (mensagem_json,))
conn.commit()

# Fechar conexão
conn.close()

def consulta_para_dicionario(query, parametros=None):
    """
    Executa uma consulta SQL e retorna os resultados como lista de dicionários
    
    Args:
        query: string com a consulta SQL
        parametros: tupla com parâmetros para a consulta (opcional)
    
    Returns:
        Lista de dicionários, onde cada dicionário representa uma linha
    """
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
    cursor = conn.cursor()
    
    if parametros:
        cursor.execute(query, parametros)
    else:
        cursor.execute(query)
    
    # Converter cada linha para dicionário
    resultados = [dict(linha) for linha in cursor.fetchall()]
    
    # Para a coluna 'mensagem', converter de JSON para dicionário Python
    for resultado in resultados:
        if 'mensagem' in resultado:
            resultado['mensagem'] = json.loads(resultado['mensagem'])
    
    conn.close()
    return resultados