import sqlite3
from typing import Optional, Dict, Any, List

class GerenciadorUsuarios:
    def __init__(self, db_name: str = '../hospital.db'):
        """
        Inicializa o gerenciador de usuários e garante a criação da tabela 'usuarios'.

        Args:
            db_name (str): Caminho para o arquivo do banco de dados SQLite.
        """
        self.db_name = db_name
        self._criar_tabela()

    def _conectar(self):
        """
        Abre uma nova conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Objeto de conexão SQLite.
        """
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        """
        Cria a tabela 'usuarios' caso ela ainda não exista.
        Campos:
            - id: identificador único
            - nome: nome completo
            - email: deve ser único
            - senha: senha do usuário
            - idade: idade (opcional)
            - genero: gênero (opcional)
            - tipo: representa o perfil (ex: 0 = admin, 1 = médico, etc.)
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    idade INTEGER,
                    genero TEXT,
                    tipo INTEGER
                )
            ''')
            conn.commit()

    def inserir(self, nome: str, email: str, senha: str, tipo: int,
                idade: Optional[int] = None, genero: Optional[str] = None) -> int:
        """
        Insere um novo usuário no banco de dados.

        Args:
            nome (str): Nome completo.
            email (str): Email (único).
            senha (str): Senha (pode ser armazenada com hash futuramente).
            tipo (int): Tipo do usuário (ex: 0 = admin).
            idade (Optional[int]): Idade do usuário.
            genero (Optional[str]): Gênero do usuário.

        Returns:
            int: ID do usuário inserido, ou -1 se o email já existir.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO usuarios (nome, email, senha, idade, genero, tipo)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nome, email, senha, idade, genero, tipo))
                conn.commit()
                print(f"Usuário '{nome}' inserido com sucesso.")
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                print(f"Email '{email}' já existe no banco de dados.")
                return -1

    def consultar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Consulta usuários com base em filtros opcionais.

        Args:
            filtros (Optional[Dict[str, Any]]): Dicionário com colunas e valores a filtrar.

        Returns:
            List[Dict[str, Any]]: Lista de usuários encontrados.
        """
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
        """
        Atualiza informações de um usuário específico.

        Args:
            id_usuario (int): ID do usuário a ser atualizado.
            novos_dados (Dict[str, Any]): Campos e valores a serem modificados.
        """
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
        """
        Remove um usuário do banco de dados.

        Args:
            id_usuario (int): ID do usuário a ser removido.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            conn.commit()
            print(f"Usuário ID {id_usuario} removido com sucesso.")
    
    def obter_tipo_usuario(self, identificador: Any, por_email: bool = False) -> Optional[int]:
        """
        Retorna o tipo do usuário dado o ID ou o email.

        Args:
            identificador (Any): ID (int) ou email (str) do usuário.
            por_email (bool): Se True, busca por email. Caso contrário, por ID.

        Returns:
            Optional[int]: Tipo do usuário, ou None se não encontrado.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            if por_email:
                cursor.execute("SELECT tipo FROM usuarios WHERE email = ?", (identificador,))
            else:
                cursor.execute("SELECT tipo FROM usuarios WHERE id = ?", (identificador,))

            resultado = cursor.fetchone()
            return resultado[0] if resultado else None

    def autenticar(self, email: str, senha: str) -> Optional[Dict[str, Any]]:
        """
        Verifica se o usuário com o email e senha fornecidos existe no banco.

        Args:
            email (str): Email do usuário.
            senha (str): Senha do usuário.

        Returns:
            Optional[Dict[str, Any]]: Dicionário com os dados do usuário autenticado, ou None se inválido.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            resultado = cursor.fetchone()

            if resultado:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, resultado))
            else:
                return None
