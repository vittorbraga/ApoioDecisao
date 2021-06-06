from random import getrandbits, randint, random, choice
import random as rand

def population(n_de_individuos, n_de_itens, pesos_e_valores, peso_maximo):
    """"Cria a populacao"""
    populacao = []
    for x in range(n_de_individuos // 2): # metade da populacao vai caber dentro da mochila
        individuo_qualificado = [ 0 for x in range(n_de_itens) ] # todas as posicoes iniciam com 0
        peso = 0
        while (peso < peso_maximo): # enquanto o peso dos objetos inseridos na mochila for menor que o peso maximo inserimos o elemento na mochila
            index = rand.randrange(499) # randomicamente adicionamos um item na mochila
            peso += pesos_e_valores[index][0]
            if (peso + pesos_e_valores[index][0] < peso_maximo):
                individuo_qualificado[index] = 1
        populacao.append(individuo_qualificado)

    for x in range(n_de_individuos // 2): # a outra metade vai ser gerada randomicamente
        populacao.append([ getrandbits(1) for x in range(n_de_itens) ])
    return populacao

def fitness(individuo, peso_maximo, pesos_e_valores):
    """Faz avaliacao do individuo"""
    peso_total, utilidade_total, valor_total, fitness = 0, 0, 0, 0
    for indice, valor in enumerate(individuo):
        peso_total += (individuo[indice] * pesos_e_valores[indice][0])
        utilidade_total += (individuo[indice] * pesos_e_valores[indice][1])
        valor_total += (individuo[indice] * pesos_e_valores[indice][2])
        fitness += (individuo[indice] * (pesos_e_valores[indice][1] / pesos_e_valores[indice][2]))

    if (peso_maximo - peso_total) < 0: # se o peso do individuo for maior que a capacidade da mochila, ele sera penalizado
        return fitness / ((peso_maximo - peso_total) * 100)
    if(valor_total > 0):
        return fitness #se o peso do individuo for menor que a capacidade da mochila retorna seu valor
    return -1

def ordenar_por_fitness(populacao, peso_maximo, pesos_e_valores):
    """ordena a populacao em um array com o seu fitness e o indice do individuo no array de populacao"""
    """valores = [fitness, [index, peso_para_selecao_ranking]]"""
    valores = []
    for index in range(len(populacao)):
        valores.append(
            [fitness(populacao[index], peso_maximo, pesos_e_valores), [index, 0]]
        )
    valores.sort()
    for index in range(len(valores)):
        valores[index][1][1] = (0.9 + (10.1-0.9) * (float(index)/float(len(valores)-1))) # nesse ponto calcula o peso do individuo para
                                                                                        # usar na selecao por ranking
    valores.sort(reverse=True)
    populacao_ordenada = []
    for x in valores: # ordena o array de populacao do maior fitness para o menor fitness
        populacao_ordenada.append(populacao[x[1][0]])
    return populacao_ordenada, valores

def selecao_roleta(pais):
    """Seleciona um pai e uma mae baseado nas regras da roleta"""
    def sortear(fitness_total, indice_a_ignorar=-1): #2 parametro garante que nao vai selecionar o mesmo elemento
        """Monta roleta para realizar o sorteio"""
        roleta, acumulado, valor_sorteado = [], 0, random()

        if indice_a_ignorar!=-1: #Desconta do total, o valor que sera retirado da roleta
            fitness_total -= valores[0][indice_a_ignorar]

        for indice, i in enumerate(valores[0]):
            if indice_a_ignorar==indice: #ignora o valor ja utilizado na roleta
                continue
            acumulado += i
            roleta.append(acumulado/fitness_total)
            if roleta[-1] >= valor_sorteado:
                return indice

    valores = list(zip(*pais)) #cria 2 listas com os valores fitness e os cromossomos
    fitness_total = sum(valores[0])

    indice_pai = sortear(fitness_total)
    indice_mae = sortear(fitness_total, indice_pai)

    pai = valores[1][indice_pai]
    mae = valores[1][indice_mae]

    return pai, mae

def selecao_ranking(populacao, valores):
    """Seleciona um pai e uma mae baseado nas regras de ranking"""
    homem, mulher = [], []
    h, m = rand.uniform(0.9, 10.1), rand.uniform(0.9, 10.1)
    for x in range(len(valores)):
        if valores[x][1][1] <= h and valores[ (x if x+1 >= len(valores) else x+1) ][1][1] <= h and x > 0:
            homem = populacao[valores[x][1][0]]
            break
    for x in range(len(valores)):
        if valores[x][1][1] <= m and valores[ (x if x+1 >= len(valores) else x+1) ][1][1] <= m and x > 0:
            mulher = populacao[valores[x][1][0]]
            break
    return homem, mulher

def crossover_1_ponto(homem, mulher):
    """Metodo de cruzamento onde uma parte do novo individuo vem de um pai e o restante do outro pai"""
    filho = []
    ponto_corte = rand.randrange(len(homem)-1)
    filho = homem[:ponto_corte] + mulher[ponto_corte:]
    return filho

def crossover_2_pontos(homem, mulher):
    """Metodo de cruzamento onde a primeira parte do novo individuo vem de um pai """
    """ o meio do outro pai e o restante do primeiro pai """
    filho = []
    ponto_corte_1 = rand.randrange(len(homem)-1)
    ponto_corte_2 = rand.randint(ponto_corte_1, len(homem)-1)
    if(random() < 0.5):
        for x in range(0, ponto_corte_1):
            filho.append(homem[x])
        for x in range(ponto_corte_1, ponto_corte_2):
            filho.append(mulher[x])
        for x in range(ponto_corte_2, len(homem)):
            filho.append(homem[x])
    else:
        for x in range(0, ponto_corte_1):
            filho.append(mulher[x])
        for x in range(ponto_corte_1, ponto_corte_2):
            filho.append(homem[x])
        for x in range(ponto_corte_2, len(homem)):
            filho.append(mulher[x])
    return filho

def evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos, mutate=0.05, reproduction=1.0, selecao=1, cruzamento=1):
    """classifica cada individuo e o seu fitness"""
    pais = [ [fitness(x, peso_maximo, pesos_e_valores), x] for x in populacao if fitness(x, peso_maximo, pesos_e_valores) >= 0]
    pais.sort(reverse=True)

    # REPRODUCAO
    filhos = []
    populacao, valores = ordenar_por_fitness(populacao, peso_maximo, pesos_e_valores)
    while len(filhos) < n_de_cromossomos: # reproduz ate que a populacao seja igual a quantidade de individuos da populacao inicial
        if reproduction > random():
            if (selecao == 1): homem, mulher = selecao_roleta(pais)
            if (selecao == 2): homem, mulher = selecao_ranking(populacao, valores)
            if (cruzamento == 1): filhos.append(crossover_1_ponto(homem, mulher))
            if (cruzamento == 2): filhos.append(crossover_2_pontos(homem, mulher))

    # MUTACAO
    for individuo in filhos:
        if mutate > random(): # mutacao variavel de acordo com a taxa de cruzamento com o passar das geracoes
            pos_to_mutate = randint(0, len(individuo)-1) # posicao de mutacao variavel
            if individuo[pos_to_mutate] == 1:
                individuo[pos_to_mutate] = 0
            else:
                individuo[pos_to_mutate] = 1

    return filhos

def distancia_individuo(individuo_conjunto, individuo):
    distancia = 0
    for index in range(len(individuo_conjunto)):
        if(individuo_conjunto[index] != individuo[index]):
            distancia += 1
    return distancia

def tem_convergencia(populacao, k, y, m):
    i = 1
    conjuntos = []
    conjuntos.append([1, populacao[0]])
    while (i <= len(populacao)) and (len(conjuntos) < k):
        j = 1
        while (j <= len(conjuntos)):
            if distancia_individuo(conjuntos[j-1][1], populacao[i]) < y:
                conjuntos[j-1][0] += 1
                if conjuntos[j-1][0] > m:
                    # print(conjuntos)
                    return True
                break
            j += 1
        if j > len(conjuntos):
           conjuntos.append([1, populacao[i]])
        i += 1
    if len(conjuntos) < k:
        # print(conjuntos)
        return True
    # print(conjuntos)
    return False