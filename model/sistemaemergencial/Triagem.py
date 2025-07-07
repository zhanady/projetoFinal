from sistemaemergencial.FilaAtendimento import FilaAtendimento
from usuarios.Paciente import PacienteBuilder


class Triagem:
    # Constantes que determinam as cores do protocólo de manchester
    VERMELHA = 0
    LARANJA = 1
    AMARELA = 2
    VERDE = 3
    AZUL = 4
    FILA = FilaAtendimento.get_instancia()

    def __init__(self, paciente, escala_dor#, escala_sang
                 , escala_glascow, sinais_vitais):
        self.paciente = paciente
        self.escala_dor = escala_dor
        # self.escala_sang = escala_sang
        self.escala_glascow = escala_glascow
        self.sinais_vitais = sinais_vitais
        self.cor_pulseira = 4

    @staticmethod
    def emergencia(paciente=None):
        # retorna uma triagem com a cor da pulseira vermelha
        triagem = Triagem(paciente, None, None, None, None)
        triagem.cor_pulseira = Triagem.VERMELHA
        return triagem

    def registrar_sinais_vitais(self, sinais_vitais):
        self.sinais_vitais = sinais_vitais

    def aplicar_protocolo_manchester(self):
        # como há 5 valores, ambos vão valer uma unidade, e quanto cada um vai valer
        # vai ser determinado na base do if e else

        # Tirei os parâmetros do Gemini por não conseguir achar fontes consistentes:
        # Se o paciente tiver batimentos iguais ou maiores que 140bpm ou batimentos
        # iguais ou menores a 50, ele precisa do atendimento.
        # Se o paciente tiver batimentos iguais ou maiores que 170bpm ou batimentos
        # iguais ou menores a 40, ele precisa bastante do atendimento.

        ponto_sinais_vitais = 1
        if self.sinais_vitais >= 170 or self.sinais_vitais <= 40:
            ponto_sinais_vitais = -1
        elif self.sinais_vitais >= 140 or self.sinais_vitais <= 50:
            ponto_sinais_vitais = 0

        # Não consegui uma fonte consistente de taxa de volume sanguíneo por idades e
        # sexos, então por ora peguei os seguintes valores do Gemini:

        # Taxas de Volume de Sangue por Quilograma (ml/kg)
        #
        # Prematuros:
        # 90-100 ml/kg (algumas fontes chegam a 105 ml/kg)

        # Recém-nascidos (a termo):
        # 80-90 ml/kg (com um pico de até 105 ml/kg no primeiro mês, diminuindo depois)

        # Bebês (até 3 meses):
        # Aproximadamente 85 ml/kg

        # Crianças (acima de 3 meses):
        # Aproximadamente 75 ml/kg (algumas fontes indicam 70-80 ml/kg)

        # Adolescentes e Adultos:
        # Homens: Aproximadamente 70-75 ml/kg
        # Mulheres: Aproximadamente 60-65 ml/kg

        ponto_escala_sangue = 1
        # Se o paciente for recém-nascido
        # if self.paciente.get_idade() == 0:
        #     media_sangue = self.paciente.get_peso() * 0.09
        # Se o paciente tiver menos de 15 anos ou for masculino
        # elif self.paciente.get_idade() <= 14 or self.paciente.get_sexo() == 'M':
        #     media_sangue = self.paciente.get_peso() * 0.075
        # Se a paciente é feminina
        # else:
        #     media_sangue = self.paciente.get_peso() * 0.065

        # Perdeu mais de 30% do sangue
        # if self.escala_sang < media_sangue * 0.7:
        #     ponto_escala_sangue = -1
        # Perdeu mais de 20% do sangue
        # elif self.escala_sang < media_sangue * 0.8:
        #     ponto_escala_sangue = 0

        ponto_escala_glascow = 1
        # Se a pontuação for 3 (a menor possível), o paciente precisa muito de atendimento
        if self.escala_glascow < 4:
            ponto_escala_glascow = -1
        # Se a pontuação for menor que 10, o paciente precisa de atendimento
        elif self.escala_glascow < 10:
            ponto_escala_glascow = 0

        # Pûs uma escala genérica de dor de 1 a 10
        ponto_escala_dor = 1
        if self.escala_dor == 10:
            ponto_escala_dor = -1
        elif self.escala_dor > 6:
            ponto_escala_dor = 0

        cor_pulseira = ponto_sinais_vitais + ponto_escala_glascow + ponto_escala_dor + 1
        if cor_pulseira < 0:
            cor_pulseira = 0
        self.cor_pulseira = cor_pulseira

    # determina a cor da pulseira
    def definir_prioridade(self):
        self.aplicar_protocolo_manchester()

    def encaminhar_para_fila(self):
        Triagem.FILA.adicionar_paciente(self.paciente)

    def get_cor_pulseira(self):
        return self.cor_pulseira

if __name__ == "__main__":
    builder = (PacienteBuilder().set_cpf("1234")
               .set_nome("Josh")
               .set_idade(42)
               .set_categoria(0)
               .set_peso(74)
                )
    paciente = builder.build()
    triagem = Triagem(paciente, 7, 9, 100)
    paciente.set_triagem(triagem)
    triagem.definir_prioridade()
    print(triagem.get_cor_pulseira())

