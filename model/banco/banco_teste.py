#from model.banco.GerenciadorProfissionais import GerenciadorProfissionais
#from banco_chat import GerenciadorMensagens

#----------------testando banco fila
'''
from model.banco.gerenciador_fila import GerenciadorFila

# Criar instância
gerenciador_fila = GerenciadorFila()

# Adicionar à fila
gerenciador_fila.adicionar_paciente_fila(
    id_paciente=5,
    tipo_fila=2,  # Atendimento
    prioridade=1   # Alta
)

# Buscar fila de atendimento
fila_atendimento = gerenciador_fila.buscar_fila(
    tipo_fila=2,
    status='Pendente'
)
'''

#------------------- testando banco mensagens
'''
# Criar instância
gerenciador_msg = GerenciadorMensagens()

# Inserir mensagem
id_msg = gerenciador_msg.inserir_mensagem({
    'hora': '14:00',
    'mensagem': 'Resultados de exames disponíveis',
    'prioridade': 'alta'
})

# Buscar mensagens
todas_msg = gerenciador_msg.buscar_mensagens()
'''
#-------------------------------------- testando banco de profissionais
'''
def testar_busca():  
    gerenciador = GerenciadorProfissionais()
    
    gerenciador.inserir_dados_exemplo()
    
    resultados = gerenciador.buscar_profissionais()  # Sem filtros
    
    print("Profissionais encontrados:")
    for prof in resultados:
        print(prof)
    cardiologistas = gerenciador.buscar_profissionais(
        {'departamento': 'Cardiologia'}
    )
    print("\nCardiologistas:")
    for card in cardiologistas:
        print(card)
'''


#if __name__ == "__main__":
#    testar_busca()