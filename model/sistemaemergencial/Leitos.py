class Leitos:
    def __init__(self, numero_leito, paciente, profissional, data_entrada, data_saida):
        self.numero_leito = numero_leito
        # Paciente neste caso pode ser tanto a instância, como um identificador no
        # BD
        self.paciente = paciente
        self.profissional = profissional
        self.data_entrada = data_entrada
        self.data_saida = data_saida

    def get_numero_leito(self):
        return self.numero_leito

    def set_numero_leito(self, numero_leito):
        self.numero_leito = numero_leito

    def get_paciente(self):
        return self.paciente

    def set_paciente(self, paciente):
        self.paciente = paciente

    def get_profissional(self):
        return self.profissional

    def set_profissional(self, profissional):
        self.profissional = profissional

    def get_data_entrada(self):
        return self.data_entrada

    def set_data_entrada(self, data_entrada):
        self.data_entrada = data_entrada

    def get_data_saida(self):
        return self.data_saida

    def set_data_saida(self, data_saida):
        self.data_saida = data_saida

