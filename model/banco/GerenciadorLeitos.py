# Importações necessárias
import datetime
import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime

from sistemaemergencial.Leitos import Leitos  # Importa a classe Leitos definida em outro módulo

# Classe que gerencia os leitos hospitalares usando um banco de dados SQLite
class GerenciadorLeitos:
    def __init__(self, db_name: str = '../hospital.db'):
        """
        Inicializa a classe GerenciadorLeitos.

        Args:
            db_name (str): Caminho do banco de dados SQLite. Padrão: '../hospital.db'
        """
        self.db_name = db_name
        self._criar_tabela()  # Garante que a tabela exista ao iniciar

    def _conectar(self):
        """
        Estabelece uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Conexão ativa com o banco
        """
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        """
        Cria a tabela 'leitos' no banco de dados, caso ela ainda não exista.
        """
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

    def inserir(self, numero_leito: int, id_paciente: int, id_medico_encaminhou: int,
                data_entrada: str, data_saida: Optional[str] = None):
        """
        Insere um novo registro de leito no banco de dados.

        Args:
            numero_leito (int): Número do leito.
            id_paciente (int): ID do paciente alocado.
            id_medico_encaminhou (int): ID do médico que encaminhou.
            data_entrada (str): Data e hora da entrada no leito (formato string).
            data_saida (Optional[str]): Data e hora da saída, se houver. Padrão: None.

        Returns:
            int: ID do registro inserido.
        """
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
        """
        Consulta registros de leitos com ou sem filtros.

        Args:
            filtros (Optional[Dict[str, Any]]): Dicionário de filtros (ex: {'id_paciente': 1}).

        Returns:
            List[Dict[str, Any]]: Lista de dicionários com os registros encontrados.
        """
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

            # Ordena os resultados por número do leito e data de entrada (mais recentes primeiro)
            query += " ORDER BY numero_leito ASC, data_entrada DESC"

            cursor.execute(query, params)
            colunas = [col[0] for col in cursor.description]
            resultados = cursor.fetchall()
            return [dict(zip(colunas, linha)) for linha in resultados]

    def atualizar(self, id_leito: int, novos_dados: Dict[str, Any]):
        """
        Atualiza os dados de um leito com base no ID.

        Args:
            id_leito (int): ID do leito a ser atualizado.
            novos_dados (Dict[str, Any]): Dicionário com os campos e valores a atualizar.
        """
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
        """
        Remove um leito com base no seu ID.

        Args:
            id_leito (int): ID do leito a ser removido.
        """
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

    def remover_por_paciente(self, paciente_id: int):
        """
        Remove todos os leitos associados a um paciente.

        Args:
            paciente_id (int): ID do paciente.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM leitos WHERE id_paciente = ?", (paciente_id,))
                conn.commit()
            except Exception as e:
                print(f"❌ Erro ao remover leito: {e}")

    def isEmLeito(self, paciente_id):
        """
        Verifica se um paciente está atualmente em um leito.

        Args:
            paciente_id (int): ID do paciente.

        Returns:
            bool: True se estiver em leito, False caso contrário.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM leitos WHERE id_paciente = ?
            ''', (paciente_id,))
            return cursor.fetchone() is not None

    def isLeitosCheios(self):
        """
        Verifica se a capacidade máxima de leitos foi atingida.

        Returns:
            bool: True se houver 8 ou mais leitos ocupados.
        """
        return 8 <= len(self.consultar())

    def get_leito(self, paciente_id):
        """
        Retorna um objeto Leitos com os dados do paciente especificado.

        Args:
            paciente_id (int): ID do paciente.

        Returns:
            Leitos: Objeto com os dados do leito associado ao paciente.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT numero_leito, id_paciente, id_medico_encaminhou, data_entrada, data_saida  
                FROM leitos WHERE id_paciente = ?
            ''', (paciente_id,))
            numero_leito, id_paciente, id_medico_encaminhou, data_entrada, data_saida = cursor.fetchone()
            return Leitos(
                numero_leito,
                id_paciente,
                id_medico_encaminhou,
                datetime.strptime(data_entrada, "%Y-%m-%d %H:%M:%S"),
                datetime.strptime(data_saida, "%Y-%m-%d %H:%M:%S") if data_saida else None
            )


# Bloco de teste principal
if __name__ == "__main__":
    # Instancia o gerenciador
    leito = GerenciadorLeitos()

    # Insere um novo leito com paciente e médico (OBS: falta o argumento numero_leito, isso causará erro!)
    leito_id = leito.inserir(numero_leito=101, id_paciente=1, id_medico_encaminhou=2, data_entrada="2025-06-12 14:00:00")

    # Exibe todos os registros de leitos
    print(leito.consultar())

    # Consulta registros de leito para um paciente específico
    print(leito.consultar({'id_paciente': 1}))

    # Atualiza o leito com data de saída
    leito.atualizar(leito_id, {'data_saida': '2025-06-15 18:00:00'})

    # Remove o leito pelo ID
    leito.remover(leito_id)
