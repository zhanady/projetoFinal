import sqlite3
from typing import Optional, Dict, Any, List


class GerenciadorRelatorio:
    def __init__(self, db_name: str = '../usuarios.db'):
        self.db_name = db_name
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
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
            conn.commit()

    def inserir(self, data: str, categoria: str, quantidade: int,
                valor_total: Optional[float], observacao: Optional[str]) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO relatorio (data, categoria, quantidade, valor_total, observacao)
                VALUES (?, ?, ?, ?, ?)
            ''', (data, categoria, quantidade, valor_total, observacao))
            conn.commit()
            print(f"Registro inserido com sucesso! ID: {cursor.lastrowid}")
            return cursor.lastrowid

    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM relatorio"
            params = []

            if filtros:
                clausulas = []
                for coluna, valor in filtros.items():
                    clausulas.append(f"{coluna} = ?")
                    params.append(valor)
                query += " WHERE " + " AND ".join(clausulas)

            cursor.execute(query, params)
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, row)) for row in cursor.fetchall()]

    def atualizar(self, id_relatorio: int, novos_dados: Dict[str, Any]):
        if not novos_dados:
            print("Nenhum dado fornecido para atualização.")
            return

        with self._conectar() as conn:
            cursor = conn.cursor()
            campos = ', '.join([f"{coluna} = ?" for coluna in novos_dados])
            valores = list(novos_dados.values()) + [id_relatorio]
            cursor.execute(f'''
                UPDATE relatorio
                SET {campos}
                WHERE id = ?
            ''', valores)
            conn.commit()
            print(f"Relatório ID {id_relatorio} atualizado com sucesso.")

    def remover(self, id_relatorio: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM relatorio WHERE id = ?", (id_relatorio,))
            conn.commit()
            print(f"Relatório ID {id_relatorio} removido com sucesso.")
