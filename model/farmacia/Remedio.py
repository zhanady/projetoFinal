class Remedio:
    # Não estou convencido de que definir categorias de remédios como constantes estáticas é uma
    # boa ideia
    ANTIBIOTICO = 0
    ANTIFUNGICO = 1
    ANTIVIRAL = 2
    ANALGESICO = 3

    def __init__(self, nome, categoria):
        self.nome = nome
        self.categoria = categoria

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, categoria):
        self.categoria = categoria


