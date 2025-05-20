# pelo que foi definido, acredito que Fila deve seguir um padrão singleton,
# isto é, existir uma única instância no programa inteiro

# aí só falta implementar a lógica de ordenamento: os pacientes com pulseira vermelha
# no início da fila (lista neste caso, ou será que implementamos uma fila mesmo?) e
# os pacientes com pulseira azul no final. Se dois pacientes tem a mesma pulseira, o que
# entrou antes sempre fica em primeiro.
import datetime


class Fila:
    INSTANCIA = None

    @staticmethod
    def get_instancia():
        if Fila.INSTANCIA is None:
            Fila.INSTANCIA = Fila()
        return Fila.INSTANCIA

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

    def liberar_paciente(self, paciente):
        if paciente not in self.pacientes:
            return

        self.pacientes.remove(paciente)
        del self.lista_espera[paciente]
