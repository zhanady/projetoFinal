class Mensagem:
    def __init__(self, usuario, mensagem):
        self.usuario = usuario
        self.mensagem = mensagem

    def get_usuario(self):
        return self.usuario

    def set_usuario(self, valor):
        self.usuario = valor

    def get_mensagem(self):
        return self.mensagem

    def set_mensagem(self, valor):
        self.mensagem = valor


