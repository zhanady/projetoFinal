# pelo que foi definido, acredito que Fila deve seguir um padrão singleton,
# isto é, existir uma única instância no programa inteiro

import datetime


# Aqueles que tiverem triagem estarão nesta fila aguardando por atendimento
class FilaAtendimento:
    INSTANCIA = None

    @staticmethod
    def get_instancia():
        if FilaAtendimento.INSTANCIA is None:
            FilaAtendimento.INSTANCIA = FilaAtendimento()
        return FilaAtendimento.INSTANCIA

    def __init__(self):
        self.pacientes = []
        self.lista_espera = {}

    def get_pacientes(self):
        return self.pacientes[:]

    def get_lista_espera(self):
        return dict(self.lista_espera)

    def adicionar_paciente(self, paciente):
        if paciente in self.pacientes:
            return

        horario_entrada = datetime.datetime.now()
        self.pacientes.append(paciente)
        self.lista_espera[paciente] = horario_entrada

        self.ordernar_fila()

    def liberar_paciente(self, paciente):
        if paciente not in self.pacientes:
            return

        self.pacientes.remove(paciente)
        del self.lista_espera[paciente]

    def ordernar_fila(self):
        # 1. Ordenação por triagem
        pulseiras_vermelhas, pulseiras_laranjas, pulseiras_amarelas, pulseiras_verdes, \
            pulseiras_azuis = 0, 0, 0, 0, 0

        def logica_ordenacao_triagem(paciente):
            from project.model.sistemaemergencial.Triagem import Triagem
            gravidade = paciente.get_triagem().get_cor_pulseira()
            if gravidade == Triagem.VERMELHA:
                nonlocal pulseiras_vermelhas
                pulseiras_vermelhas += 1
            elif gravidade == Triagem.LARANJA:
                nonlocal pulseiras_laranjas
                pulseiras_laranjas += 1
            elif gravidade == Triagem.AMARELA:
                nonlocal pulseiras_amarelas
                pulseiras_amarelas += 1
            elif gravidade == Triagem.VERDE:
                nonlocal pulseiras_verdes
                pulseiras_verdes += 1
            else:
                nonlocal pulseiras_azuis
                pulseiras_azuis += 1
            return gravidade

        self.pacientes = sorted(self.pacientes, key=logica_ordenacao_triagem)

        # 2. Ordenação por datas entre pacientes de uma triagem
        def logica_ordenacao_data(paciente):
            return self.lista_espera[paciente]

        pulseiras_args = pulseiras_vermelhas, pulseiras_laranjas, pulseiras_amarelas, pulseiras_verdes, \
            pulseiras_azuis

        pacientes = []
        contador = 0
        for pulseira in pulseiras_args:
            lista_paciente = self.pacientes[contador:(contador + pulseira)]
            lista_paciente = sorted(lista_paciente, key=logica_ordenacao_data)
            contador += pulseira

            pacientes += lista_paciente

        self.pacientes = pacientes

