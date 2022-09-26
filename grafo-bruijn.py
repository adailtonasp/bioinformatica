
k = 3

lista_entrada=("ATT","GCC","CAT","TTG","CCA","TGC","ATC","TCC","TGA","GAC","CAT","ATG","CCA")

string_saida= ""

class node:
    def __init__(self,value):    
        self.value = value
        self.lista_entrada = []
        self.lista_saida = []

class arco:
    def __init__(self,node_saida,node_entrada,rotulo):
        self.node_saida = node_saida
        self.node_entrada = node_entrada
        self.rotulo = rotulo

lista_node = []
lista_arco = []

for i in lista_entrada:
    prefixo = i[:k-1]
    sufixo = i[1:k]
    
    node_p = None
    node_s = None

    if prefixo not in [lista_node[i].value for i in range(len(lista_node))]:
        node_p = node(prefixo)
        lista_node.append(node_p)
    else:
        node_p = [lista_node[x] for x in range(len(lista_node)) if lista_node[x].value == prefixo][0]

    if sufixo not in [lista_node[i].value for i in range(len(lista_node))]:
        node_s = node(sufixo)
        lista_node.append(node_s)
    else:
        node_s = [lista_node[x] for x in range(len(lista_node)) if lista_node[x].value == sufixo][0]

    arco_c = arco(node_p,node_s,i)

    arco_c.node_saida.lista_saida.append(arco_c)

    arco_c.node_entrada.lista_entrada.append(arco_c)

    lista_arco.append(arco_c)

init_node = None
final_node = None

for i in lista_node:
    if len(i.lista_entrada) - len(i.lista_saida) < 0: 
        init_node = i

    if len(i.lista_entrada) - len(i.lista_saida) > 0:
        final_node = i

    if init_node != None and final_node != None:
        break

node_atual = init_node

#correcao para inicio do caminho no ciclo
while(len(node_atual.lista_saida) == 1 and len(lista_arco) > 0):
    string_saida = string_saida + node_atual.value

    lista_arco.remove(node_atual.lista_saida[0])

    node_atual = node_atual.lista_saida[0].node_entrada  

#correcao para finalizacao do caminho no ciclo
string_saida_anexo = ""
while(len(final_node.lista_entrada) == 1 and len(lista_arco) > 0):
    string_saida_anexo = final_node.value + string_saida_anexo

    lista_arco.remove(final_node.lista_entrada[0])

    final_node = final_node.lista_entrada[0].node_saida

arco_atual = node_atual.lista_saida[0]

ciclo = []

while (len(lista_arco) != 0):

    while(node_atual.value != arco_atual.node_entrada.value):
        ciclo.append(arco_atual)
        node_atual = arco_atual.node_entrada
        arco_atual = node_atual.lista_saida[0]
        node_atual.lista_saida.remove(arco_atual)

    for i in ciclo:
        lista_arco.remove(i)
    
    ciclo = []

input()