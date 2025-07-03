import datetime


class Chat:
    # o atributo mensagens vai ser um dict, cujas chaves são o horário de envio de uma
    # mensagem e os valores são as mensagens propriamente ditas
    def __init__(self, usuarios):
        self.usuarios = usuarios
        self.mensagens = {}
        self.contador = 0

    def get_usuarios(self):
        return self.usuarios[:]

    def get_mensagens(self):
        return dict(self.mensagens)

    def adicionar_mensagem(self, mensagem):
        self.contador += 1
        self.mensagens[self.contador] = (mensagem, datetime.datetime.now())
        # if horario_envio is None:
        #     horario_envio = datetime.datetime.now()
        #
        # se nosso programa for single-thread ou não realizar o acesso do chat em uma
        # base de dados externa, teoricamente ele nunca vai entrar nesse loop
        # while horario_envio in self.mensagens:
        #     horario_envio.replace(microsecond=horario_envio.microsecond + 1)
        #
        # self.mensagens[horario_envio] = mensagem

    def remover_mensagem(self, mid):
        for chave, valor in self.mensagens.keys():
            if chave == mid:
                del self.mensagens[chave]
                return

    def adicionar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def remover_usuario(self, usuario):
        self.usuarios.remove(usuario)
