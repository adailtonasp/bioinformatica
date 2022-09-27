k = 3

#lista_entrada=("ATT","GCC","CAT","TTG","CCA","TGC","ATC","TCC","TGA","GAC","CAT","ATG","CCA")

with open("entrada_bruijn.txt", 'r') as file_w:
    lista_entrada = file_w.readline().split(",")
        

class node:
    grau_entrada = 0
    grau_saida = 0
    def __init__(self,value):
        self.value = value

class arco:
    def __init__(self,node_saida,node_entrada,rotulo):
        node_saida.grau_saida += 1
        node_entrada.grau_entrada += 1
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

    lista_arco.append(arco_c)

init_node = None
final_node = None

#identificar nos de inicio e fim
i = 0
while(True):
    if lista_node[i].grau_entrada > lista_node[i].grau_saida:
        final_node = lista_node[i]
    if lista_node[i].grau_entrada < lista_node[i].grau_saida:
        init_node = lista_node[i]
    i += 1
    if(init_node != None and final_node != None):
        break
    
node_atual = init_node

string_saida= ""

try:
    string_saida = string_saida + node_atual.value
except:
    print("Nao foi possivel definir um no inicial")
    exit()

#correcao para inicio do caminho no ciclo
while node_atual.grau_saida == 1 and node_atual.grau_entrada == 0:

    #encontra um arco cuja saida e o no atual
    arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual][0]

    #remova esse arco da lista de arcos e atualiza o grau

    lista_arco.remove(arco_c)

    #nao e necessario atualizar o grau de cada no ?

    node_atual.grau_saida -= 1

    node_atual = arco_c.node_entrada

    node_atual.grau_entrada -= 1

    string_saida = string_saida + node_atual.value[-1]

#correcao para finalizacao do caminho no ciclo
string_saida_anexo = ""
while final_node.grau_entrada == 1 and final_node.grau_saida == 0:
    
    string_saida_anexo = final_node.value[-1] + string_saida_anexo

    arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_entrada == final_node][0]

    lista_arco.remove(arco_c)

    final_node.grau_entrada -= 1

    final_node = arco_c.node_saida

    final_node.grau_saida -= 1

arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual][0]

ciclo_node_v = [] #ciclo de valores de no

while (len(lista_arco) != 0):

    while True:
        ciclo_node_v.append(node_atual.value)
        #atualiza as referencias dos nos que envolver o arco atual

        node_atual.grau_saida -= 1

        node_atual = arco_c.node_entrada

        node_atual.grau_entrada -= 1

        string_saida = string_saida + node_atual.value[-1]

        lista_arco.remove(arco_c)

        if(len(lista_arco) == 0):
            break

        arco_c = [lista_arco[x] for x in range(len(lista_arco)) if lista_arco[x].node_saida == node_atual][0]

        if node_atual.value in ciclo_node_v:
            break
            
    ciclo_node_v = []

string_saida = string_saida + string_saida_anexo
input(string_saida)