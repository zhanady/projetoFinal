import sqlite3
from typing import Optional, Dict, Any, List


class GerenciadorPacientes:
    def __init__(self, db_name: str = 'hospital.db'):
        self.db_name = db_name
        self._criar_tabelas()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabelas(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            # Tabela usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    email TEXT
                )
            ''')

            # Tabela pacientes
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
            conn.commit()

    def inserir_usuario(self, nome: str, cpf: str, telefone: Optional[str], email: Optional[str]) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios (nome, cpf, telefone, email)
                VALUES (?, ?, ?, ?)
            ''', (nome, cpf, telefone, email))
            conn.commit()
            cursor.execute("SELECT id FROM usuarios WHERE cpf = ?", (cpf,))
            return cursor.fetchone()[0]

    def inserir_paciente(self, usuario_id: int, data_nascimento: str, sexo: str,
                         tipo_sanguineo: str, endereco: str, status: str) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO pacientes (usuario_id, data_nascimento, sexo, tipo_sanguineo, endereco, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (usuario_id, data_nascimento, sexo, tipo_sanguineo, endereco, status))
            conn.commit()
            print(f"Paciente vinculado ao usuário ID {usuario_id} inserido.")
            return cursor.lastrowid

    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT p.*, u.nome, u.cpf, u.telefone, u.email
                FROM pacientes p
                JOIN usuarios u ON p.usuario_id = u.id
            '''
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

    def atualizar(self, id_paciente: int, novos_dados: Dict[str, Any]):
        if not novos_dados:
            print("Nenhum dado para atualizar.")
            return

        with self._conectar() as conn:
            cursor = conn.cursor()
            campos = ', '.join([f"{k} = ?" for k in novos_dados])
            valores = list(novos_dados.values()) + [id_paciente]
            cursor.execute(f'''
                UPDATE pacientes
                SET {campos}
                WHERE id = ?
            ''', valores)
            conn.commit()
            print(f"Paciente ID {id_paciente} atualizado.")

    def remover(self, id_paciente: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
            conn.commit()
            print(f"Paciente ID {id_paciente} removido.")
