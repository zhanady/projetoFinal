from projetoFinal.model.farmacia.Farmacia import Farmacia


class Prescricao:
    def __init__(self, paciente, medico, remedios):
        self.paciente = paciente
        self.medico = medico
        # "remedios" vai ser um dicionário. Instâncias de Remedio serão as
        # chaves e a quantidade deles serão os valores
        self.remedios = remedios

    def get_paciente(self):
        return self.paciente

    def get_medico(self):
        return self.medico

    # retorna uma cópia da lista de remédios
    def get_remedios(self):
        return dict(self.remedios)

    def adicionar_medicamento(self, remedio):
        self.remedios.append(remedio)

    def remover_medicamento(self, remedio):
        self.remedios.remove(remedio)

    # esse comportamento deve ter relação com a farmácia, mas eu não sei exatamente
    # o que ele faz. caso ela verifique se a farmácia possui a quantidade de remédios
    # exigida na prescrição, devemos adicionar na prescrição essa informação (quantidade
    # de remédios)
    def validar_dose(self):
        pass

    # pelo que entendi, esse método abstrai o método liberar_remedios da instância
    # de Farmacia
    def enviar_para_farmacia(self):
        return Farmacia.INSTANCIA.liberar_remedios(self)
