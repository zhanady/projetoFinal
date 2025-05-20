class Usuario:
    # categorias
    ADMIN = 0
    FUNCIONARIO = 1
    CLIENTE = 2

    def __init__(self, login, senha, categoria):
        # verifica se a categoria posta como argumento existe
        if not 0 <= categoria <= 2:
            pass
        self.login = login
        self.senha = senha
        self.categoria = categoria
        self.chats = []

    def verificar_login(self, login):
        return self.login == login

    def verificar_senha(self, senha):
        return self.senha == senha

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, categoria):
        self.categoria = categoria

    # retorna uma cópia da lista com chats
    def get_chats(self):
        return self.chats[:]

    def adicionar_chat(self, chat):
        self.chats.append(chat)

    def remover_chat(self, chat):
        self.chats.remove(chat)

    # não sei exatamente o que isso faz
    def verificar_nivel(self):
        pass

