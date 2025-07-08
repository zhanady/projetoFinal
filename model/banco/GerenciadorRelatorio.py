import sqlite3
from typing import Optional, Dict, Any, List

class GerenciadorRelatorio:
    def __init__(self, db_name: str = '../usuarios.db'):
        """
        Inicializa o gerenciador de relatórios.

        Args:
            db_name (str): Caminho para o banco de dados SQLite onde será criada/tomada a tabela de relatórios.
        """
        self.db_name = db_name
        self._criar_tabela()  # Garante que a tabela 'relatorio' existe

    def _conectar(self):
        """
        Estabelece uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Objeto de conexão SQLite.
        """
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        """
        Cria a tabela 'relatorio' caso ela ainda não exista no banco.
        Campos:
            - id: identificador do relatório
            - data: data do evento (texto)
            - categoria: tipo ou natureza do relatório
            - quantidade: quantidade envolvida (ex: itens, atendimentos, etc)
            - valor_total: valor monetário total associado
            - observacao: texto adicional livre
        """
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
        """
        Insere um novo relatório na tabela.

        Args:
            data (str): Data do evento ou movimentação (formato livre, ex: '2025-07-07').
            categoria (str): Tipo de entrada (ex: 'medicamento', 'atendimento', etc).
            quantidade (int): Quantidade associada ao evento.
            valor_total (Optional[float]): Valor monetário total da operação (opcional).
            observacao (Optional[str]): Comentário adicional (opcional).

        Returns:
            int: ID do relatório recém-inserido.
        """
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
        """
        Consulta registros de relatório com ou sem filtros.

        Args:
            filtros (Optional[Dict[str, Any]]): Dicionário com colunas e valores a filtrar (ex: {"categoria": "medicamento"}).

        Returns:
            List[Dict[str, Any]]: Lista de relatórios como dicionários.
        """
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
        """
        Atualiza um ou mais campos de um relatório existente.

        Args:
            id_relatorio (int): ID do relatório que será atualizado.
            novos_dados (Dict[str, Any]): Dicionário com os campos a atualizar e seus novos valores.
        """
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
        """
        Remove um relatório do banco com base no ID.

        Args:
            id_relatorio (int): ID do relatório que será excluído.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM relatorio WHERE id = ?", (id_relatorio,))
            conn.commit()
            print(f"Relatório ID {id_relatorio} removido com sucesso.")
