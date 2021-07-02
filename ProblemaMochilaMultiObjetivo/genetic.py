from random import getrandbits, random, randint
import random as rand
import sys

def population(n_de_individuos, n_de_itens, pesos_e_valores, peso_maximo):
    populacao = []
    for x in range(n_de_individuos // 2): # metade da populacao vai caber dentro da mochila
        individuo_qualificado = [ 0 for x in range(n_de_itens) ]
        peso = 0
        while (peso < peso_maximo):
            index = rand.randrange(n_de_itens - 1)
            peso += pesos_e_valores[index][0]
            if (peso + pesos_e_valores[index][0] < peso_maximo):
                individuo_qualificado[index] = 1
        populacao.append([(0, [0, 0, 0]), individuo_qualificado])

    for x in range(n_de_individuos // 2): # a outra metade vai ser gerada randomicamente
        individuo = [ getrandbits(1) for x in range(n_de_itens) ]
        populacao.append([(0, [0, 0, 0]), individuo])
    return populacao

def evaluation(individuo, peso_maximo, pesos_e_valores):
    peso_total, utilidade_total, valor_total, dominancia = 0, 0, 0, 0
    for indice, valor in enumerate(individuo):
        peso_total += (individuo[indice] * pesos_e_valores[indice][0])
        utilidade_total += (individuo[indice] * pesos_e_valores[indice][1])
        valor_total += (individuo[indice] * pesos_e_valores[indice][2])
    return dominancia, [peso_total, utilidade_total, valor_total]

def nsga2(pais):
    for index in range(len(pais)):
        for index2 in range(len(pais)):
            if pais[index] != pais[index2]:
                peso = pais[index][0][1][0]
                utilidade = pais[index][0][1][1]
                valor = pais[index][0][1][2]
                i_peso = pais[index2][0][1][0]
                i_utilidade = pais[index2][0][1][1]
                i_valor = pais[index2][0][1][2]
                if(utilidade >= i_utilidade and valor <= i_valor):
                    pais[index2] = [(pais[index2][0][0] + 1, pais[index2][0][1]),pais[index2][1]]
                # else:
                #     pais[index] = [(pais[index][0][0] + 1, pais[index][0][1]),pais[index][1]]
    for index in range(len(pais)):
        if pais[index][0][1][0] == 0 or pais[index][0][1][1] == 0 or pais[index][0][1][2] == 0 or pais[index][0][1][0] > 12:
            pais[index] = [(999999, pais[index][0][1]),pais[index][1]]
    return pais

def selecao_ranking(populacao):
    p = -1
    i_ranking = []
    for x in range(len(populacao)):
        if p != populacao[x][0][0]:
            i_ranking.append(populacao[x][0][0])
            p = populacao[x][0][0]
    i_ranking.sort(reverse=True)
    valores = []
    for x in range(len(i_ranking)):
        valores.append([
            0.9 + (10.1-0.9) * (x/(len(i_ranking) - 1)),
            [i_ranking[x]]
        ])
    homem, mulher = [], []
    hp, mp = -1, -1
    h, m = rand.uniform(0.9, 10.1), rand.uniform(0.9, 10.1)
    for x in range(len(valores)):
        if valores[x][0] <= h and valores[ (x if x+1 >= len(valores) else x+1) ][0] >= h:
            hp = valores[x][1][0]
            break
    for x in range(len(valores)):
        if valores[x][0] <= m and valores[ (x if x+1 >= len(valores) else x+1) ][0] >= m:
            mp = valores[x][1][0]
            break
    for x in range(len(populacao)):
        if populacao[x][0][0] == hp:
            homem = populacao[x]
            break
    for x in range(len(populacao)):
        if populacao[x][0][0] == mp:
            mulher = populacao[x]
            break
    return homem, mulher

def crossover_2_pontos(homem, mulher):
    filho = []
    ponto_corte_1 = rand.randrange(len(homem[1])-1)
    ponto_corte_2 = rand.randint(ponto_corte_1, len(homem[1])-1)
    if(random() < 0.5):
        for x in range(0, ponto_corte_1):
            filho.append(homem[1][x])
        for x in range(ponto_corte_1, ponto_corte_2):
            filho.append(mulher[1][x])
        for x in range(ponto_corte_2, len(homem[1])):
            filho.append(homem[1][x])
    else:
        for x in range(0, ponto_corte_1):
            filho.append(mulher[1][x])
        for x in range(ponto_corte_1, ponto_corte_2):
            filho.append(homem[1][x])
        for x in range(ponto_corte_2, len(homem[1])):
            filho.append(mulher[1][x])
    return [(0, [0, 0, 0]), filho]

def evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos, mutate=0.05, reproduction=1.0, selecao=2, cruzamento=2):
    """classifica cada individuo e o seu fitness"""
    pais = [ [evaluation(x[1], peso_maximo, pesos_e_valores), x[1]] for x in populacao]
    pais = nsga2(pais)
    pais.sort()

    # REPRODUCAO
    filhos = []
    while len(filhos) < n_de_cromossomos: # reproduz ate que a populacao seja igual a quantidade de individuos da populacao inicial
        if reproduction > random():
            # if (selecao == 1): homem, mulher = selecao_roleta(pais)
            if (selecao == 2): homem, mulher = selecao_ranking(pais)
            # if (cruzamento == 1): filhos.append(crossover_1_ponto(homem, mulher))
            if (cruzamento == 2): filhos.append(crossover_2_pontos(homem, mulher))

    # MUTACAO
    for individuo in filhos:
        if mutate > random(): # mutacao variavel de acordo com a taxa de cruzamento com o passar das geracoes
            pos_to_mutate = randint(0, len(individuo[1])-1) # posicao de mutacao variavel
            if individuo[1][pos_to_mutate] == 1:
                individuo[1][pos_to_mutate] = 0
            else:
                individuo[1][pos_to_mutate] = 1

    nova_populacao = pais + filhos
    nova_populacao = [ [evaluation(x[1], peso_maximo, pesos_e_valores), x[1]] for x in nova_populacao]
    nova_populacao = nsga2(nova_populacao)
    nova_populacao.sort()
    return nova_populacao[:int(n_de_cromossomos/2)]

def metodo_borda(menor_dominancia):
    matriz = []
    for x in range(3):
        matriz.append([])
        for y in range(len(menor_dominancia)):
            matriz[x].append(menor_dominancia[y][0][1][x])

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            sys.stdout.write(str(round(matriz[i][j], 2)) + ' ')
        print()

    # utilidade
    matriz.append([])
    for i in range(len(matriz[1])):
        matriz[3].append(0)

    for i in range(len(matriz[1])):
        classificacao = 1
        for j in range(len(matriz[1])):
            if matriz[1][i] < matriz[1][j]:
                classificacao += 1
        matriz[3][i] = classificacao

    # peso
    matriz.append([])
    for i in range(len(matriz[1])):
        matriz[4].append(0)
    for i in range(len(matriz[2])):
        classificacao = 1
        for j in range(len(matriz[2])):
            if matriz[2][i] > matriz[2][j]:
                classificacao += 1
        matriz[4][i] = classificacao

    # peso
    matriz.append([])
    for i in range(len(matriz[1])):
        matriz[5].append(0)
    for i in range(len(matriz[1])):
        matriz[5][i] = matriz[3][i] + matriz[4][i]

    print("------------------------------")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            sys.stdout.write(str(round(matriz[i][j], 2)) + ';')
        print()

