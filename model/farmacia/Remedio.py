class Remedio:
    def __init__(self, medicamento, principio_ativo, concentracao):
        self.medicamento = medicamento
        self.principio_ativo = principio_ativo
        self.concentracao = concentracao

    def get_medicamento(self):
        return self.medicamento

    def set_medicamento(self, medicamento):
        self.medicamento = medicamento

    def get_principio_ativo(self):
        return self.principio_ativo

    def set_principio_ativo(self, principio_ativo):
        self.principio_ativo = principio_ativo

    def get_concentracao(self):
        return self.concentracao

    def set_concentracao(self, concentracao):
        self.concentracao = concentracao

