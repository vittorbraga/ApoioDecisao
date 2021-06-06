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
geracoes = 200                                  #                                                                #
tempo_execucao = 5 # minutos                    #                     Variaveis de definicoes                    #
n_de_itens = len(pesos_e_valores)               #                                                                #
taxa_cruzamento_variavel = 1.0                  #                                                                #
taxa_mutacao_variavel = 0.05                    ##################################################################
operador_selecao = 2                            # 1 = roleta / 2 = ranking
operador_cruzamento = 2                         # 1 = crossover_1_ponto / 2 = crossover_2_pontos
tecnica_populacao = 2                           # 1 = substituicao / 2 = elitismo
k, y, m = 4, 4, 5

#EXECUCAO DOS PROCEDIMENTOS
populacao = population(n_de_cromossomos, n_de_itens, pesos_e_valores, peso_maximo)  # gerar a populacao inicial
populacao, valores = ordenar_por_fitness(populacao, peso_maximo, pesos_e_valores)
f = fitness(populacao[0], peso_maximo, pesos_e_valores)
itens = ""
for indice in range(len(populacao[0])):
    if (populacao[0][indice] == 1):
        itens += str(indice) + ", "
peso_total, utilidade_total, valor_total = 0, 0, 0
for indice, valor in enumerate(populacao[0]):
    peso_total += (populacao[0][indice] * pesos_e_valores[indice][0])
    utilidade_total += (populacao[0][indice] * pesos_e_valores[indice][1])
    valor_total += (populacao[0][indice] * pesos_e_valores[indice][2])
historico_maior_fitness = [[f, 0, itens, peso_total, utilidade_total, valor_total]]     # armazena o fitness do melhor individuo da populacao
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
    # historico_maior_fitness.append(fitness(populacao[0], peso_maximo, pesos_e_valores)) # armazena o fitness do melhor individuo da populacao
    f = fitness(populacao[0], peso_maximo, pesos_e_valores)
    itens = ""
    for indice in range(len(populacao[0])):
        if (populacao[0][indice] == 1):
            itens += str(indice) + ", "
    peso_total, utilidade_total, valor_total = 0, 0, 0
    for indice, valor in enumerate(populacao[0]):
        peso_total += (populacao[0][indice] * pesos_e_valores[indice][0])
        utilidade_total += (populacao[0][indice] * pesos_e_valores[indice][1])
        valor_total += (populacao[0][indice] * pesos_e_valores[indice][2])
    historico_maior_fitness.append([f, i, itens, peso_total, utilidade_total, valor_total])     # armazena o fitness do melhor individuo da populacao

    if i %20 == 0:
        print("verificar convergencia")
        if tem_convergencia(populacao, k, y, m):
            print("convergencia na geracao " + str(i))
            for x in range(len(populacao) // 2):
                populacao.append([ getrandbits(1) for x in range(n_de_itens) ])

# #PRINTS DO TERMINAL
for indice in range(len(historico_maior_fitness)):
   print ("Geracao: ", str(historico_maior_fitness[indice][1]).zfill(3)," | Maior fitness na mochila: ", round(historico_maior_fitness[indice][0], 5)," | Peso Total: ", round(historico_maior_fitness[indice][3], 3)," | Utilidade Total: ", historico_maior_fitness[indice][4]," | Valor Total: ", round(historico_maior_fitness[indice][5], 3)," | Itens na Mochila: ", historico_maior_fitness[indice][2])

# print("\nExemplos de boas solucoes: ")
# for i in range(5):
#     print(populacao[i])

#GERADOR DE GRAFICO
h = []
for x in range(len(historico_maior_fitness)):
    h.append(historico_maior_fitness[x][0])
from matplotlib import pyplot as plt
plt.plot(range(len(h)), h)
plt.grid(True, zorder=0)
plt.title("Problema da mochila")
plt.xlabel("Geracao")
plt.ylabel("Maior fitness")
plt.show()