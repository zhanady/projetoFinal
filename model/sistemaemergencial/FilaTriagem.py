import datetime
import time

from model.usuarios.Paciente import PacienteBuilder


# Fila de espera para a triagem. Fica nesta fila aqueles que não tem uma triagem definida
class FilaTriagem:
    INSTANCIA = None

    @staticmethod
    def get_instancia():
        if FilaTriagem.INSTANCIA is None:
            FilaTriagem.INSTANCIA = FilaTriagem()
        return FilaTriagem.INSTANCIA

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


# TESTE

if __name__ == "__main__":
    paciente1 = PacienteBuilder() \
        .set_idade(17) \
        .set_nome("Anderson") \
        .set_cpf("092.671.679-44") \
        .build()

    paciente2 = PacienteBuilder() \
        .set_idade(25) \
        .set_nome("André") \
        .set_cpf("473.769.539-49") \
        .build()

    filaTriagem = FilaTriagem.get_instancia()

    filaTriagem.adicionar_paciente(paciente1)
    time.sleep(0.3)

    filaTriagem.adicionar_paciente(paciente2)

    lista_espera = filaTriagem.get_lista_espera()
    for item in lista_espera.keys():
        print("%s entrou as %s" % (item.get_nome(), lista_espera[item]))

    print("======================")

    filaTriagem.liberar_paciente(paciente1)

    lista_espera = filaTriagem.get_lista_espera()
    for item in lista_espera.keys():
        print("%s entrou as %s" % (item.get_nome(), lista_espera[item]))
