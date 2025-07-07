import inspect

from usuarios.Usuario import Usuario


class Paciente(Usuario):
    @staticmethod
    def get_builder():
        return PacienteBuilder()

    def __init__(self, login, senha, categoria, cpf, nome, idade, sexo, tipo_sang,
                 contato_emg, triagem, historico, id):
        super().__init__(login, senha, categoria)
        self.cpf = cpf
        self.nome = nome

        self.idade = idade
        self.sexo = sexo
        self.tipo_sang = tipo_sang
        self.contato_emg = contato_emg
        self.triagem = triagem
        self.historico = historico

        self.id = id

    # Cadastrar aonde? Na fila ou no sistema de usuários?
    def cadastrar(self):
        pass

    def atualizar_dados(self, nome=None, idade=None, sexo=None, tipo_sang=None, peso=None, contato_emg=None, gravidade=None,
                        historico=None):
        # Deve haver uma maneira melhor de criar este método em vez de 8 IFs em sequência.
        if nome is not None:
            self.nome = nome

        if idade is not None:
            self.idade = idade

        if sexo is not None:
            self.sexo = sexo

        if tipo_sang is not None:
            self.tipo_sang = tipo_sang

        if contato_emg is not None:
            self.contato_emg = contato_emg

        if gravidade is not None:
            self.triagem = gravidade

        if historico is not None:
            self.historico = historico

    def obter_historico_medico(self):
        return self.get_historico()

    def verificar_prioridade_triagem(self):
        return self.triagem.get_cor_pulseira()

    def get_cpf(self):
        return self.cpf

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_idade(self):
        return self.idade

    def get_sexo(self):
        return self.sexo

    def get_tipo_sang(self):
        return self.tipo_sang

    def get_contato_emg(self):
        return self.contato_emg

    def get_triagem(self):
        return self.triagem

    def get_historico(self):
        return self.historico

    def set_triagem(self, triagem):
        self.triagem = triagem


# Como Paciente tem vários atributos, achei conveniente criar uma classe Builder só para
# instânciar ela.
class PacienteBuilder:
    def __init__(self):
        self.login = ""
        self.senha = ""
        self.categoria = 0
        self.nome = ""
        self.cpf = ""
        self.idade = ""
        self.sexo = 'M'
        self.tipo_sang = None
        self.peso = None
        self.contato_emg = []
        self.gravidade = None
        self.historico = []
        self.id = 0

    def build(self):
        return Paciente(self.login, self.senha, self.categoria,
                        self.cpf, self.nome, self.idade, self.sexo, self.tipo_sang, self.contato_emg,
                        self.gravidade,
                        self.historico, self.id)

    def set_nome(self, nome):
        self.nome = nome
        return self

    def set_login(self, login):
        self.login = login
        return self

    def set_senha(self, senha):
        self.senha = senha
        return self

    def set_categoria(self, categoria):
        self.categoria = categoria
        return self

    def set_idade(self, idade):
        self.idade = idade
        return self

    def set_sexo(self, sexo):
        self.sexo = sexo
        return self

    def set_tipo_sang(self, tipo_sang):
        self.tipo_sang = tipo_sang
        return self

    def set_contato_emg(self, contato_emg):
        self.contato_emg = contato_emg
        return self

    def set_gravidade(self, gravidade):
        self.gravidade = gravidade
        return self

    def set_cpf(self, cpf):
        self.cpf = cpf
        return self

    def set_id(self, id):
        self.id = id
        return self

    def set_historico(self, historico):
        self.historico = historico
        return self

    def add_historico(self, internacao):
        if self.historico is None:
            self.historico = [internacao]
            return self
        self.historico.append(internacao)
        return self


if __name__ == "__main__":
    print(inspect.signature(PacienteBuilder().build().atualizar_dados))
    print()
