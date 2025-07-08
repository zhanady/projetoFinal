class Mensagem:
    def __init__(self, usuario, mensagem, data):
        self.usuario = usuario
        self.mensagem = mensagem
        self.data = data

    def get_usuario(self):
        return self.usuario

    def set_usuario(self, valor):
        self.usuario = valor

    def get_mensagem(self):
        return self.mensagem

    def set_mensagem(self, valor):
        self.mensagem = valor

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data


