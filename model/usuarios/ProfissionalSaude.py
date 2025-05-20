from Usuario import Usuario


class ProfissionalSaude(Usuario):
    def __init__(self, login, senha, categoria, residencia, crm):
        super().__init__(login, senha, categoria)

        # um médico ou enfermeira não pode ser cliente (ou singularmente um cliente)
        if not categoria != Usuario.CLIENTE:
            pass

        self.residencia = residencia
        self.crm = crm

    def get_residencia(self):
        return self.residencia

    def set_residencia(self, residencia):
        self.residencia = residencia

    def get_crm(self):
        return self.crm

    def set_crm(self, crm):
        self.crm = crm




