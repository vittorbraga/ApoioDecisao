from genetic import *
import datetime
import csv

f = open('Problema_da_Mochila.csv','r')         #################################################################
reader = csv.reader(f, delimiter=';')           #                                                                #
pesos_e_valores = []                            #                                                                #
for row in reader:                              #                                                                #
    try:                                        #                                                                #
        pesos_e_valores.append([                #           Esse bloco faz a leitura do arquivo csv              #
            float(row[1].replace(',', '.')),    #                    [peso,utilidade,valor]                      #
            int(row[2].replace(',', '.')),      #                                                                #
            float(row[3].replace(',', '.'))     #                                                                #
        ])                                      #                                                                #
    except:                                     #                                                                #
        print("")                               ##################################################################

peso_maximo = 12                                ##################################################################
n_de_cromossomos = 1000                         #                                                                #
geracoes = 100                                  #                                                                #
tempo_execucao = 5 # minutos                    #                     Variaveis de definicoes                    #
n_de_itens = len(pesos_e_valores)               #                                                                #
taxa_cruzamento_variavel = 1.0                  #                                                                #
taxa_mutacao_variavel = 0.05                    ##################################################################
operador_selecao = 1                            # 1 = roleta / 2 = ranking
operador_cruzamento = 1                         # 1 = crossover_1_ponto / 2 = crossover_2_pontos
tecnica_populacao = 1                           # 1 = substituicao / 2 = elitismo

#EXECUCAO DOS PROCEDIMENTOS
populacao = population(n_de_cromossomos, n_de_itens, pesos_e_valores, peso_maximo)  # gerar a populacao inicial
populacao, valores = ordenar_por_fitness(populacao, peso_maximo, pesos_e_valores)
historico_maior_fitness = [fitness(populacao[0], peso_maximo, pesos_e_valores)]     # armazena o fitness do melhor individuo da populacao
data_parada = datetime.datetime.now() + datetime.timedelta(minutes=tempo_execucao)
i = 0
while ((datetime.datetime.now() < data_parada) and (i <= geracoes)): # a parada da evolucao vai acontecer po tempo de execucao
                                                                    #ou numero de geracoes
    i += 1
    filhos = evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos,taxa_mutacao_variavel, taxa_cruzamento_variavel,
        operador_selecao, operador_cruzamento)
    if taxa_cruzamento_variavel >= 0.8 and i%2 == 0: # a taxa de cruzamento diminui ate o limite de 80%
        taxa_cruzamento_variavel -= 0.005
    if taxa_mutacao_variavel <= 0.8: # a taxa de mutacao aumenta ate o limite de 20%
        taxa_mutacao_variavel += 0.005
    if tecnica_populacao == 2: # Aplicar elitismo, deixando os 10 melhores individuos da populacao anterior
        populacao, valores = ordenar_por_fitness(populacao, peso_maximo, pesos_e_valores)
        for index in range(100): # adiciona os 100 melhores individuos da populacao antiga na nova populacao
            filhos.append(populacao[index])
    populacao = filhos
    populacao, valores = ordenar_por_fitness(populacao, peso_maximo, pesos_e_valores)
    historico_maior_fitness.append(fitness(populacao[0], peso_maximo, pesos_e_valores)) # armazena o fitness do melhor individuo da populacao

# #PRINTS DO TERMINAL
for indice in enumerate(historico_maior_fitness):
   print ("Geracao: ", indice," | Maior fitness na mochila: ", historico_maior_fitness[indice])

# print("\nExemplos de boas solucoes: ")
# for i in range(5):
#     print(populacao[i])