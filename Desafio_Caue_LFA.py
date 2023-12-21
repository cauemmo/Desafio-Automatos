import string  # importa a biblioteca String


# Cauê Mendonça Magela do Ó/rgm:43558

# Reune todos os dados e retorna o AFD e seus dados
def conversor():
    estados = input('Informe os estados separados por espaco : ').split(" ")
    verificacao = True
    while (verificacao):
        estado_inicial = input('Informe o estado inicial valido: ')
        if (estado_inicial in estados):  # Verifica se existe o estado inicial fornecido em estados
            verificacao = False
        else:
            print("Estado inicial invalido!\n")

    auxDelta = estado_inicial

    verificacao = True
    while (verificacao):
        estados_finais = input('Informe os estados finais separados por espacos:').split(" ")
        if (set(estados_finais).issubset(set(estados))):  # verifica se esta contido em estados
            verificacao = False
        else:
            print("Estados finais não aceitos...")

    alfab = input('Informe o alfabeto separados por espaco:').split(" ")

    # inserindo o 'ε' no alfabeto
    tam = len(alfab) + 1
    alfab.insert(tam, 'ε')
    delta = transicao(estados, alfab)

    # a partir daqui ocorre o processo de criacao de fecho e em seguida a conversao AFN para
    auxDelta = auxDelta.split(" ")

    fecho = {}
    fecho = cria_fecho(fecho, auxDelta, delta, alfab)

    alfab.remove('ε')

    # pega estados finais afd
    estados_finais_afd = []
    for i in fecho.values():
        for j in estados_finais:
            if (j in i):
                estados_finais_afd.append(i)  # adicionando

    estado_inicial_afd = fecho[0];

    print("\nConversao AFN para AFD:\n")
    DeltaAFD = {}
    DeltaAFD = cria_DeltaAFD(DeltaAFD, fecho, alfab, delta)

    print("\nEstado Inicial: ", estado_inicial_afd)

    print("\nEstados Finais: ")
    for x in estados_finais_afd:
        print(x)

    # Simlificado AFD
    simpleDelta, statesEndAFD = AFD_simples(DeltaAFD, alfab, fecho, estados, estados_finais_afd)

    stateFirstAFD = estados[0]

    return estados, stateFirstAFD, statesEndAFD, simpleDelta, alfab


# montador da transição
def transicao(estados, alfab):
    D = {}
    for i in estados:
        for j in alfab:

            verificacao = True
            while (verificacao):
                estado_destino = input('D(%s,%s): ' % (i, j)).split(" ")
                D[i, j] = estado_destino
                if ((set(D[i, j]).issubset(set(estados))) or (set('v').issubset(set(D[i, j])))):
                    verificacao = False
                else:
                    print("transicao não pertence ao conjunto de estados!")
    return D


# Função que retorna o aux para montar nosso fecho
def auxFecho(auxDelta, delta):
    auxList = []
    auxList = auxDelta
    for x in auxList:
        if ("v" not in delta[x, 'ε']):
            auxDelta += delta[x, 'ε']
    return auxDelta


# Transforma o Delta
def transforma_Delta(alfab, auxDelta, Geral, delta):
    for i in alfab:
        auxGeral = []
        for j in auxDelta:
            if ("ε" not in i):
                if ("v" not in delta[j, i]):
                    auxGeral += delta[j, i]
                Geral[i] = auxGeral
    return Geral


# Função que monta o fecho
def cria_fecho(fecho, auxDelta, delta, alfab):
    auxfecho = []
    auxfecho = auxFecho(auxDelta, delta)

    fecho[0] = auxfecho
    x = 0
    verificacao = True
    while (verificacao):
        aux = {}
        if (x <= len(fecho) - 1):
            aux = transforma_Delta(alfab, fecho[(x)], aux, delta)

        else:
            verificacao = False

        for j in aux.values():
            auxfecho = []
            auxfecho = auxFecho(j, delta)
            auxfecho = sorted(set(auxfecho))

            if (auxfecho not in fecho.values()):
                lenfecho = len(fecho)
                fecho[lenfecho] = auxfecho
        x = x + 1
    return fecho


# monta o delta e mostra as transições
def cria_DeltaAFD(DeltaAFD, lock, alfabeto, delta):
    for i in lock.values():
        for j in alfabeto:
            auxDeltaAfd = {}
            auxDeltaAfd = transforma_Delta(j, i, auxDeltaAfd, delta)
            for k in auxDeltaAfd.values():
                auxList = []
                auxList = auxFecho(k, delta)
                auxList = sorted(set(auxList))

                DeltaAFD[tuple(i), j] = auxList
            if (i == []):
                DeltaAFD[tuple(i), j] = i

            print(i, " transicao ", j, ": ", DeltaAFD[tuple(i), j])
    return DeltaAFD


# Função que deixa simples o Delta AFD
def AFD_simples(delta, alfabeto, lock, states, novofim):
    newDelta = {}
    keysLock = []
    statesEndAFD = []

    keysLock = (list(lock.keys())).copy()  # lista com as chaves do dicionario de fecho

    cont = 0
    for i in lock.values():
        for j in alfabeto:
            for x in keysLock:
                if (delta[tuple(i), j] == lock[x]):
                    indexLock = x
                for k in novofim:
                    if (k == lock[x]):
                        if (states[x] not in statesEndAFD):
                            statesEndAFD.append(states[x])  # usando o append evita repetições na nossa lista

            newDelta[states[cont], j] = states[indexLock]
        cont += 1
    return newDelta, statesEndAFD


def aux_Modificar(alfab, q, delta):
    aux = {}
    for al in alfab:
        aux[al] = delta[q, al]
    return aux


# modifica o delta para auxiliar na transformação para ER
def Modificar(delta, estados, alfab):
    aux = {}
    for q in estados:
        aux[q] = aux_Modificar(alfab, q, delta)
    return aux


def repetir(delta, state):
    for q in delta:
        if delta[q] == state:
            return q


# Adiciona os Parenteses
def add_Parenteses(delta):
    aux = {}
    for q in delta:
        aux['(' + q + ')'] = delta[q]
    return aux


def setar_est_ini(delta, alpha, state):
    list_loop = is_loop(delta, alpha)
    list_not_loop = not_loop(delta, alpha)

    new_q = ''  # nova chave
    aux = {}

    for q, j in delta[state].items():
        if j == alpha:
            new_q += key_loop(q, list_loop)
            aux = get_aux(new_q, delta, list_not_loop, alpha)

    for q, j in delta[state].items():
        if j != alpha:
            aux[q] = j
    return aux


# Uniao da Expressão
def uniao(delta):
    aux = {}
    for q in delta:
        if delta[q] not in aux.values():
            aux[q] = delta[q]
        else:
            new_key = repetir(aux, delta[q]) + 'U' + q  # Faz a união
            aux[new_key] = delta[q]
            del aux[repetir(aux, delta[q])]  # del serve para deletar elementos

            aux = add_Parenteses(aux)

    return aux


# Função que tira os parenteses sobrando, os ε da uniao
def simplificar_ER(ER):
    lista_ER = list(filter(None, ER.split('ε')))
    tam_ListaER = len(lista_ER)
    Str = ''

    if tam_ListaER > 1:
        for i in range(tam_ListaER):
            if i + 1 < tam_ListaER:
                if (not (lista_ER[i][-1] in ['U', ')', '('] and lista_ER[i + 1][0] in ['U', ')', '('])):
                    Str += lista_ER[i]
    else:
        Str = lista_ER[0]

    return Str


# Retorna uma lista sem loop faz loop
def not_loop(delta, alpha):
    list_looped = []
    for q in delta[alpha]:
        if delta[alpha][q] != alpha and delta[alpha][q] != '':
            list_looped.append(q)
    return list_looped


# Retorna uma lista com os que faz loop
def is_loop(delta, alpha):
    list_looped = []
    for q in delta[alpha]:
        if delta[alpha][q] == alpha:
            list_looped.append(q)
    return list_looped


# Pega as chaves que fazem loops
def key_loop(key, list_looped):
    new_key = key
    for i in list_looped:
        new_key += i + '*'

    return new_key


# Pega o novo estado
def get_aux(key, delta, list_aux, alpha):
    new_qs = {}
    for i in list_aux:
        new_qs[key + i] = delta[alpha][i]
    return new_qs


def reajuste(delta, alpha):
    aux = delta[alpha]
    for key in aux:
        q = delta[alpha][key]
        if q != alpha and q != '':
            for i in delta[q]:
                if i in delta[q] and delta[q][i] == alpha:
                    delta[q] = setar_est_ini(delta, alpha, q)
                    delta[q] = uniao(delta[q])


def modifica_est(delta, estados_finais, est_transicaoE):
    delta['qs'] = {'ε': est_transicaoE}
    delta['qa'] = {}

    for est_fin in estados_finais:
        delta[est_fin]['ε'] = 'qa'


def transforma(transicao):
    if len(transicao) < 3:
        return transicao

    estado_inicial = transicao['qs']

    # ordena todos os estados
    estado_inicial = sorted(estado_inicial.keys(), key=len)

    for alfab in estado_inicial:
        if alfab in transicao['qs'] and transicao['qs'][alfab] != 'qa':
            UltAlfab = transicao['qs'][alfab]
            transicao['qs'] = setar_est_ini(transicao, UltAlfab, 'qs')
            transicao['qs'] = uniao(transicao['qs'])

            reajuste(transicao, UltAlfab)

            del transicao[UltAlfab]
            transforma(transicao)


def ajuste(delta):
    for est in delta:
        delta[est] = uniao(delta[est])

def main():
    loop = True
    while (loop):
        estados, estado_inicial, estados_finais, Delta, alfab = conversor()

        aux_a = Modificar(Delta, estados, alfab)

        ajuste(aux_a)

        modifica_est(aux_a, estados_finais, estado_inicial)
        transforma(aux_a)
        print("\nMODELO ER:\n")
        for q in aux_a['qs']:
            ER = simplificar_ER(q)
            print("ER: {", ER, "}")

        print("\n\nDeseja adicionar mais AF?")
        print("\n1-SIM\n")
        print("2-NAO\n")
        validacao = True
        while (validacao):
            opcao = int(input())

            if (opcao != 1 and opcao != 2):
                print("Opcao Invalida, tente novamente!!!\n\n")

            else:
                if (opcao == 1):
                    validacao = False
                else:
                    validacao = False
                    loop = False

if __name__ == "__main__":
    main()

"""""   
TESTE ENTRADAS

A B C
A
A B
0 1
D(A,0): A
D(A,1): B
D(A,ε): v
D(B,0): c
transicao não pertence ao conjunto de estados!
D(B,0): C
D(B,1): B
D(B,ε): v
D(C,0): C
D(C,1): C
D(C,ε): v


SAÍDAS -> 
conversao AFN para AFD:

['A']  transicao  0 :  ['A']
['A']  transicao  1 :  ['B']
['B']  transicao  0 :  ['C']
['B']  transicao  1 :  ['B']
['C']  transicao  0 :  ['C']
['C']  transicao  1 :  ['C']

Estado Inicial:  ['A']

Estados Finais:
['A']
['B']

MODELO ER:

ER: { (0*11*U0* }"""