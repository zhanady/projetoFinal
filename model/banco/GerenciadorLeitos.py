import sqlite3
from typing import Optional, List, Dict, Any


class GerenciadorLeitos:
    def __init__(self, db_name: str = 'hospital.db'):
        self.db_name = db_name
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leitos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_leito INTEGER,
                    id_paciente INTEGER,
                    id_medico_encaminhou INTEGER,
                    data_entrada TEXT,
                    data_saida TEXT
                )
            ''')

            conn.commit()

    def inserir(self, numero_leito: int, id_paciente: int, id_medico_encaminhou: int, data_entrada: str, data_saida: Optional[str] = None):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO leitos (numero_leito, id_paciente, id_medico_encaminhou, data_entrada, data_saida)
                VALUES (?, ?, ?, ?, ?)
            ''', (numero_leito, id_paciente, id_medico_encaminhou, data_entrada, data_saida))
            conn.commit()
            print(f"Leito inserido com sucesso! ID: {cursor.lastrowid}")
            return cursor.lastrowid


    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM leitos"
            params = []

            if filtros:
                clausulas = []
                for coluna, valor in filtros.items():
                    clausulas.append(f"{coluna} = ?")
                    params.append(valor)
                query += " WHERE " + " AND ".join(clausulas)

            # Ordena por número do leito e data de entrada
            query += " ORDER BY numero_leito ASC, data_entrada DESC"

            cursor.execute(query, params)
            colunas = [col[0] for col in cursor.description]
            resultados = cursor.fetchall()
            return [dict(zip(colunas, linha)) for linha in resultados]


    def atualizar(self, id_leito: int, novos_dados: Dict[str, Any]):
        if not novos_dados:
            print("⚠ Nenhum dado fornecido para atualização.")
            return

        with self._conectar() as conn:
            cursor = conn.cursor()
            campos = ', '.join([f"{col} = ?" for col in novos_dados])
            valores = list(novos_dados.values()) + [id_leito]
            try:
                cursor.execute(f'''
                    UPDATE leitos
                    SET {campos}
                    WHERE id = ?
                ''', valores)
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"✅ Leito ID {id_leito} atualizado com sucesso.")
                else:
                    print(f"⚠ Leito ID {id_leito} não encontrado.")
            except Exception as e:
                print(f"❌ Erro ao atualizar leito: {e}")


    def remover(self, id_leito: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM leitos WHERE id = ?", (id_leito,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"🗑 Leito ID {id_leito} removido com sucesso.")
                else:
                    print(f"⚠ Leito ID {id_leito} não encontrado para remoção.")
            except Exception as e:
                print(f"❌ Erro ao remover leito: {e}")


'''
# Instanciar a classe
leito = GerenciadorLeitos()

# Inserir um novo leito
leito_id = leito.inserir(id_paciente=1, id_medico_encaminhou=2, data_entrada="2025-06-12")

# Consultar todos
print(leito.consultar())

# Consultar com filtro
print(leito.consultar({'id_paciente': 1}))

# Atualizar dados
leito.atualizar(leito_id, {'data_saida': '2025-06-15'})

# Remover leito
leito.remover(leito_id)
'''