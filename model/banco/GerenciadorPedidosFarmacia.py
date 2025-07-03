import sqlite3
from datetime import datetime
from projetoFinal.model.banco.GerenciadorFarmacias import *

class GerenciadorPedidosFarmacia:
    def __init__(self, db_name='../hospital.db'):
        self.db_name = db_name
        self.farmacia = GerenciadorFarmacia(db_name)

        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos_farmacia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            campos = list(dados.keys())
            valores = list(dados.values())
            placeholders = ','.join(['?'] * len(dados))

            cursor.execute(f'''
                INSERT INTO pedidos_farmacia ({','.join(campos)})
                VALUES ({placeholders})
            ''', valores)
            conn.commit()
            return cursor.lastrowid

    def buscar_pedidos_pendentes(self):
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
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
            return [dict(row) for row in cursor.fetchall()]

    def confirmar_pedido(self, pedido_id: int, medicamento: str, quantidade: int) -> bool:
        """
        Marca o pedido como finalizado e atualiza o estoque do medicamento usando GerenciadorFarmacia.
        """
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()

                # 1. Verifica o estoque atual via nome
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
                if estoque_atual < quantidade:
                    print(f"Estoque insuficiente para '{medicamento}'.")
                    return False

                # 2. Atualiza o estoque usando o GerenciadorFarmacia
                novo_estoque = estoque_atual - quantidade
                sucesso = self.farmacia.atualizar_estoque(id_medicamento, novo_estoque)
                if not sucesso:
                    print("Erro ao atualizar estoque.")
                    return False

                # 3. Marca pedido como finalizado
                cursor.execute('UPDATE pedidos_farmacia SET status = ? WHERE id = ?', ('finalizado', pedido_id))

                conn.commit()
                return True

        except Exception as e:
            print(f"Erro ao confirmar pedido: {e}")
            return False

