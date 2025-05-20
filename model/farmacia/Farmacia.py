# pelo que foi definido, acredito que Farmacia deve seguir um padrão singleton,
# isto é, existir uma única instância no programa inteiro

class Farmacia:
    INSTANCIA = None

    @staticmethod
    def get_instancia(remedios):
        if Farmacia.INSTANCIA is None:
            Farmacia.INSTANCIA = Farmacia(remedios)
        return Farmacia.INSTANCIA

    # remedios será um dicionário, cujas chaves serão os remédios e os valores serão
    # a quantidade desses remédios no estoque
    def __init__(self, remedios=None):
        if remedios is None:
            remedios = {}
        self.remedios = remedios

    # retorna uma cópia do estoque
    def get_remedios(self):
        return dict(self.remedios)

    def adicionar_remedio(self, remedio):
        if remedio in self.remedios:
            self.remedios[remedio] += 1
            return
        self.remedios[remedio] = 1

    # visto que a classe Prescricao não está completa, este método é apenas uma idéia
    # de seu comportamento.
    def liberar_remedios(self, prescricao):
        remedios_no_estoque = []

        for remedio in prescricao.get_remedios():
            if remedio not in self.remedios:
                return False
            elif self.remedios[remedio] == 0:
                return False
            remedios_no_estoque.append(remedio)

        for remedio in remedios_no_estoque:
            self.remedios[remedio] -= 1

        return True

    # ainda não definimos nenhum processamento temporal, então deixei esse método
    # quieto
    def atualizar_estoque(self):
        pass
