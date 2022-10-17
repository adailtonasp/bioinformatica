import time
import sys

class node:
    grau_entrada = 0
    grau_saida = 0

    def __init__(self, value):
        self.value = value

class arco:
    def __init__(self, node_saida, node_entrada, rotulo):
        node_saida.grau_saida += 1
        node_entrada.grau_entrada += 1
        self.node_saida = node_saida
        self.node_entrada = node_entrada
        self.rotulo = rotulo

def criaGrafo(lista_entrada, lista_arco, lista_node, k):
    for i in lista_entrada:
        prefixo = i[:k-1]
        sufixo = i[1:k]

        node_p = None
        node_s = None

        if prefixo not in [lista_node[i].value for i in range(len(lista_node))]:
            node_p = node(prefixo)
            lista_node.append(node_p)
        else:
            node_p = [lista_node[x] for x in range(
                len(lista_node)) if lista_node[x].value == prefixo][0]

        if sufixo not in [lista_node[i].value for i in range(len(lista_node))]:
            node_s = node(sufixo)
            lista_node.append(node_s)
        else:
            node_s = [lista_node[x] for x in range(
                len(lista_node)) if lista_node[x].value == sufixo][0]

        arco_c = arco(node_p, node_s, i)

        lista_arco.append(arco_c)

def getIniEnd(lista_node):
    init_node = None
    final_node = None

    # identificar nos de inicio e fim
    i = 0
    while(True):
        if lista_node[i].grau_entrada > lista_node[i].grau_saida:
            final_node = lista_node[i]
        if lista_node[i].grau_entrada < lista_node[i].grau_saida:
            init_node = lista_node[i]
        i += 1
        if(init_node != None and final_node != None):
            break

    return init_node, final_node

# correcao para inicio do caminho no ciclo
# correcao para loops no inicio
def corteIni(lista_arco, node_atual):

    string_saida = ""

    string_saida = string_saida + node_atual.value

    arco_l = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual and lista_arco[x].node_entrada == node_atual]

    while True:

        for i in arco_l:
            string_saida = string_saida + node_atual.value[-1]

            node_atual.grau_entrada -= 1

            node_atual.grau_saida -= 1

            lista_arco.remove(i)

        while node_atual.grau_saida == 1 and node_atual.grau_entrada == 0:

            arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual][0]

            lista_arco.remove(arco_c)

            node_atual.grau_saida -= 1

            node_atual = arco_c.node_entrada

            node_atual.grau_entrada -= 1

            string_saida = string_saida + node_atual.value[-1]

        arco_l = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual and lista_arco[x].node_entrada == node_atual]

        if len(arco_l) == 0:
            break

    return string_saida, node_atual

# correcao para finalizacao do caminho no ciclo
# correcao para loops no final
def corteFinal(lista_arco, final_node):

    string_saida_anexo = ""

    arco_l = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == final_node and lista_arco[x].node_entrada == final_node]

    while True:
        #print("Resolvendo correcoes de finalizacao")
        # loops
        for i in arco_l:
            string_saida_anexo = final_node.value[-1] + string_saida_anexo

            final_node.grau_entrada -= 1

            final_node.grau_saida -= 1

            lista_arco.remove(i)

        # linear
        while final_node.grau_entrada == 1 and final_node.grau_saida == 0:

            string_saida_anexo = final_node.value[-1] + string_saida_anexo

            arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_entrada == final_node][0]

            lista_arco.remove(arco_c)

            final_node.grau_entrada -= 1

            final_node = arco_c.node_saida

            final_node.grau_saida -= 1

        arco_l = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == final_node and lista_arco[x].node_entrada == final_node]

        if len(arco_l) == 0:
            break

    return string_saida_anexo, final_node

def cicloEuleriano(lista_arco, node_atual, final_node):
    string_saida = ""

    # arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual][0]

    ciclo_node_v = []  # ciclo de valores de no

    arco_caminho = []

    avoid_arco = []

    while (len(lista_arco) != 0):

        while True:
            # resolve loop
            for i in [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual and lista_arco[x].node_entrada == node_atual]:
                string_saida = string_saida + node_atual.value[-1]

                node_atual.grau_entrada -= 1

                node_atual.grau_saida -= 1

                lista_arco.remove(i)

            arco_c = [lista_arco[x] for x in range(len(
                lista_arco)) if lista_arco[x].node_saida == node_atual and lista_arco[x] not in avoid_arco][0]

            ciclo_node_v.append(node_atual.value)

            arco_caminho.append(arco_c)

            node_atual.grau_saida -= 1

            node_atual = arco_c.node_entrada

            node_atual.grau_entrada -= 1

            string_saida = string_saida + node_atual.value[-1]

            lista_arco.remove(arco_c)

            if node_atual.value in ciclo_node_v:
                break
            elif ((node_atual == final_node) and (node_atual.grau_saida == node_atual.grau_entrada == 0)):
                break
            elif ((node_atual == final_node) and (node_atual.grau_saida == 0)):
                # um caminho sem saida foi escolhido - faca rollback
                for i in range(len(arco_caminho)):
                    lista_arco.append(arco_caminho[i])
                    string_saida = string_saida[:-1]
                    avoid_arco.append(arco_caminho[i])

                node_atual = arco_caminho[0].node_saida

                arco_caminho = []
                ciclo_node_v = []

        ciclo_node_v = []

        avoid_arco = []

    return string_saida

def main():

    start = time.time()

    with open(sys.argv[1], 'r') as file_w:
        lista_entrada = file_w.readline().split(",")

    # lista_entrada=["ATT","GCC","CAT","TTG","CCA","TGC","ATC","TCC","TGA","GAC","CAT","ATG","CCA"]
    # lista_entrada=["AAGG","AGGG","ATGG","ATGG","GATG","GGAT","GGGG","GGGT","GGTA","GGTG","GGTG","GTAA","GTGA","GTGG","TAAG","TGGA","TGGT","TGGT"]
    # lista_entrada=["GAA","ATT","AAG","TGG","GGG","TTG","AGT","AAT","TGA","GTG"]

    lista_entrada.sort()

    k = len(lista_entrada[0])

    lista_node = []
    lista_arco = []

    criaGrafo(lista_entrada, lista_arco, lista_node, k)

    init_node, final_node = getIniEnd(lista_node)

    inicio, init_node = corteIni(lista_arco, init_node)

    final, final_node = corteFinal(lista_arco, final_node)

    meio = cicloEuleriano(lista_arco, init_node, final_node)

    resultado = inicio + meio + final

    # print(resultado)
    with open("adailton_silva_palhano.txt", 'w') as file_w:
        file_w.write(resultado)
    print("k:", k)
    print("tamanho entrada:", len(lista_entrada))
    print("tamanho saida:", len(resultado))
    print("tempo:", time.time()-start)

if __name__ == "__main__":
    main()