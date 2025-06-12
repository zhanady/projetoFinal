import sqlite3
from typing import Optional, Dict, Any, List


class GerenciadorUsuarios:
    def __init__(self, db_name: str = 'hospital.db'):
        self.db_name = db_name
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
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
            conn.commit()

    def inserir(self, nome: str, email: str, senha: str,
                idade: Optional[int] = None, genero: Optional[str] = None) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO usuarios (nome, email, senha, idade, genero)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nome, email, senha, idade, genero))
                conn.commit()
                print(f"Usuário '{nome}' inserido com sucesso.")
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                print(f"Email '{email}' já existe no banco de dados.")
                return -1

    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM usuarios"
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

    def atualizar(self, id_usuario: int, novos_dados: Dict[str, Any]):
        if not novos_dados:
            print("Nenhum dado fornecido para atualização.")
            return

        with self._conectar() as conn:
            cursor = conn.cursor()
            campos = ', '.join([f"{k} = ?" for k in novos_dados])
            valores = list(novos_dados.values()) + [id_usuario]
            cursor.execute(f'''
                UPDATE usuarios
                SET {campos}
                WHERE id = ?
            ''', valores)
            conn.commit()
            print(f"Usuário ID {id_usuario} atualizado com sucesso.")

    def remover(self, id_usuario: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            conn.commit()
            print(f"Usuário ID {id_usuario} removido com sucesso.")
