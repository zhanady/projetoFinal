import sqlite3
from typing import Optional, Dict, Any, List
from banco.GerenciadorFila import *

class GerenciadorPacientes:
    def __init__(self, db_name: str = 'hospital.db'):
        self.db_name = db_name
        self._criar_tabelas()
        self.gerenciadorFila = GerenciadorFila()


    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabelas(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    data_nascimento TEXT,
                    sexo TEXT,
                    tipo_sanguineo TEXT,
                    endereco TEXT,
                    status TEXT NOT NULL DEFAULT 'ativo'
                )
            ''')
            conn.commit()

    def inserir_paciente(self, nome: str, cpf: str, telefone: Optional[str], email: Optional[str],
                            data_nascimento: str, sexo: str, tipo_sanguineo: str,
                            endereco: str, status: str = 'ativo') -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO pacientes
                (nome, cpf, telefone, email, data_nascimento, sexo, tipo_sanguineo, endereco, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, telefone, email, data_nascimento, sexo, tipo_sanguineo, endereco, status))
            conn.commit()
            id_paciente = cursor.lastrowid

        # Adiciona paciente na fila de triagem (tipo_fila=0)
        if self.gerenciadorFila and id_paciente:
            self.gerenciadorFila.adicionar_paciente_fila(id_paciente=id_paciente, tipo_fila=0, prioridade=3)

        return id_paciente

    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM pacientes'
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

    def remover(self, id_paciente: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
            conn.commit()

    def encerrar_atendimento(self, id_paciente: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE pacientes
                SET status = 'desativo'
                WHERE id = ?
            ''', (id_paciente,))
            conn.commit()
