k = 3

lista_entrada=("ATT","GCC","CAT","TTG","CCA","TGC","ATC","TCC","TGA","GAC","CAT","ATG","CCA")

class node:
    lista_entrada = []
    lista_saida = []
    def __init__(self,value):    
        self.value = value

class arco:
    node_saida = node()
    node_entrada = node()
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

    #vinculo de arco e nos

    #node_p.lista_saida.append(arco_c)

    #node_s.lista_entrada.append(arco_c)

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

string_saida= ""

try:
    string_saida = string_saida + node_atual.value
except:
    print("Nao foi possivel definir um no inicial")
    exit()
#correcao para inicio do caminho no ciclo
while(len(node_atual.lista_saida) == 1 and len(lista_arco) > 0):

    arco_c = lista_arco.pop(lista_arco.index(node_atual.lista_saida[0])) #pode ser mais simples

    node_atual.lista_saida.remove(arco_c)

    node_atual = node_atual.lista_saida[0].node_entrada

    node_atual.lista_entrada.remove(arco_c)

    string_saida = string_saida + node_atual.value[-1]
#correcao para finalizacao do caminho no ciclo
string_saida_anexo = ""
while(len(final_node.lista_entrada) == 1 and len(lista_arco) > 0):
    
    string_saida_anexo = final_node.value[-1] + string_saida_anexo

    arco_c = lista_arco.pop(lista_arco.index(final_node.lista_entrada[0])) #pode ser mais simples

    final_node.lista_entrada.remove(arco_c)

    final_node = final_node.lista_entrada[0].node_saida

    final_node.lista_saida.remove(arco_c)

arco_c = node_atual.lista_saida[0] #o primeiro dos arcos que estao saindo do no

ciclo_node_v = [] #ciclo de valores de no

while (len(lista_arco) != 0):

    while True:
        ciclo_node_v.append(node_atual.value)
        #atualiza as referencias dos nos que envolver o arco atual
        node_atual.lista_saida.remove(arco_c)
        node_atual = arco_c.node_entrada
        node_atual.lista_entrada.remove(arco_c)
        arco_c = node_atual.lista_saida[0]
        string_saida = string_saida + node_atual.value[-1]
        if node_atual.value in ciclo_node_v:
            break
    
    ciclo_node_v = []

string_saida = string_saida + string_saida_anexo

input(string_saida)