import sqlite3
from datetime import datetime
from banco.GerenciadorFarmacias import *  # Importa o gerenciador de farmácia para manipular o estoque

class GerenciadorPedidosFarmacia:
    def __init__(self, db_name='../hospital.db'):
        """
        Inicializa o gerenciador de pedidos da farmácia.

        Args:
            db_name (str): Caminho para o banco de dados SQLite.
        """
        self.db_name = db_name
        self.farmacia = GerenciadorFarmacia(db_name)  # Instância para gerenciar estoque de medicamentos
        self._criar_tabela()

    def _conectar(self):
        """
        Estabelece uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: conexão ativa com o banco.
        """
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        """
        Cria a tabela de pedidos da farmácia no banco de dados, se ainda não existir.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos_farmacia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paciente_id INTEGER NOT NULL,
                    profissional_id INTEGER NOT NULL,
                    medicamento TEXT NOT NULL,
                    principio_ativo TEXT,
                    concentracao TEXT,
                    quantidade_solicitada INTEGER NOT NULL,
                    urgencia TEXT DEFAULT 'media',
                    status TEXT DEFAULT 'pendente',
                    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def registrar_pedido(self, dados: dict) -> int:
        """
        Insere um novo pedido de medicamento. Exemplo de `dados`:
        {
            "medicamento": "Dipirona",
            "principio_ativo": "Dipirona Sódica",
            "concentracao": "500mg",
            "quantidade_solicitada": 20,
            "urgencia": "alta"
        }
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            campos = list(dados.keys())  # Nomes das colunas a inserir
            valores = list(dados.values())  # Valores correspondentes
            placeholders = ','.join(['?'] * len(dados))  # Cria os "?" para o SQL

            cursor.execute(f'''
                INSERT INTO pedidos_farmacia ({','.join(campos)})
                VALUES ({placeholders})
            ''', valores)
            conn.commit()
            return cursor.lastrowid

    def buscar_pedidos_pendentes(self):
        """
        Retorna todos os pedidos com status 'pendente', ordenados por prioridade de urgência
        (alta, média, baixa) e pela data da solicitação (mais antigos primeiro).

        Returns:
            List[dict]: Lista de pedidos pendentes.
        """
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row  # Permite acessar resultados como dicionário
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM pedidos_farmacia
                WHERE status = 'pendente'
                ORDER BY
                    CASE urgencia
                        WHEN 'alta' THEN 1
                        WHEN 'media' THEN 2
                        ELSE 3
                    END,
                    data_solicitacao ASC
            ''')
            return [dict(row) for row in cursor.fetchall()]  # Converte linhas em dicionários

    def confirmar_pedido(self, pedido_id: int, medicamento: str, quantidade: int) -> bool:
        """
        Finaliza um pedido de farmácia, atualiza o estoque do medicamento e marca o pedido como concluído.

        Args:
            pedido_id (int): ID do pedido na tabela `pedidos_farmacia`.
            medicamento (str): Nome do medicamento ou princípio ativo.
            quantidade (int): Quantidade a ser retirada do estoque.

        Returns:
            bool: True se o pedido foi processado com sucesso, False caso contrário.
        """
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()

                # 1. Verifica o estoque atual pelo nome ou princípio ativo
                cursor.execute('''
                    SELECT id, quantidade FROM farmacia 
                    WHERE LOWER(medicamento) = LOWER(?) 
                    OR LOWER(principio_ativo) = LOWER(?)
                ''', (medicamento, medicamento))

                row = cursor.fetchone()
                print(f"Buscando '{medicamento}'... Resultado: {row}")

                if not row:
                    print(f"Medicamento '{medicamento}' não encontrado.")
                    return False

                id_medicamento, estoque_atual = row

                # 2. Verifica se há estoque suficiente
                if estoque_atual < quantidade:
                    print(f"Estoque insuficiente para '{medicamento}'.")
                    return False

                # 3. Atualiza o estoque com o novo valor (estoque - quantidade solicitada)
                novo_estoque = estoque_atual - quantidade
                sucesso = self.farmacia.atualizar_estoque(id_medicamento, novo_estoque)
                if not sucesso:
                    print("Erro ao atualizar estoque.")
                    return False

                # 4. Marca o pedido como finalizado
                cursor.execute('UPDATE pedidos_farmacia SET status = ? WHERE id = ?', ('finalizado', pedido_id))

                conn.commit()
                return True

        except Exception as e:
            print(f"Erro ao confirmar pedido: {e}")
            return False
