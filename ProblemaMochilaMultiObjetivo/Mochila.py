from genetic import *
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

peso_maximo = 12
n_de_cromossomos = 1000
geracoes = 100
n_de_itens = len(pesos_e_valores)

populacao = population(n_de_cromossomos, n_de_itens, pesos_e_valores, peso_maximo)  # gerar a populacao inicial
historico = []
for gen in range(geracoes):
    print("Geracao: " + str(gen+1))
    filhos = evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos)
    historico.append(filhos[0])
    populacao = filhos

# #PRINTS DO TERMINAL
for indice in range(len(historico)):
    itens = ""
    for x in range(len(historico[indice][1])):
        if(historico[indice][1][x] == 1):
            itens += str(x+1) + ", "
    print ("Geracao: ", indice+1,
            " | Dominancia: ", historico[indice][0][0],
            " | Peso Total: ", historico[indice][0][1][0],
            " | Utilidade Total: ", historico[indice][0][1][1],
            " | Valor Total: ", historico[indice][0][1][2],
            " | Itens na Mochila: ", itens
        )

print("------------------------")
pareto = populacao[0][0][0]
menor_dominancia = []
indice = 0
while pareto == populacao[indice][0][0]:
    menor_dominancia.append(populacao[indice])
    itens = ""
    for x in range(len(populacao[indice][1])):
        if(populacao[indice][1][x] == 1):
            itens += str(x+1) + ", "
    print (" | Dominancia: ", populacao[indice][0][0],
            " | Peso Total: ", populacao[indice][0][1][0],
            " | Utilidade Total: ", populacao[indice][0][1][1],
            " | Valor Total: ", populacao[indice][0][1][2],
            " | Itens na Mochila: ", itens
        )
    indice += 1

borda = metodo_borda(menor_dominancia)