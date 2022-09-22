# Implementação do pareamento de bruijn

# Enumere cada entrada k-mer(d,m)
# d é o tamanho da virtualizaçao
# m é o tamanho da string a ser processado
# n é  o tamanho da entrada

# Produza cada nó separado onde cada nó é dividido em elemento a e elemento b

# Para cada elemento a/b de cada nó verifique se existe alguem nó com elemento b/a igual

# Se existir vincule ese outro nó ao nó atual e prossiga a verificação

# Identifique a raíz da arvore montada - no com elemento a vazio/nulo

# Monte a matriz de pareamento com tamanho igual a n x (2 * m + d) + n - 1 << verificar
# inicialize com valor nulo representativo

# preencha seguindo o algoritimo convencional

# fim

k = 3

lista_entrada=("ATT","GCC","CAT","TTG","CCA","TGC","ATC","TCC","TGA","GAC","CAT","ATG","CCA")

class node:
    def __init__(self,value):    
        self.value = value
        self.grau_entrada = 0
        self.grau_saida = 0

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

    arco_c.node_saida.grau_saida += 1

    arco_c.node_entrada.grau_entrada += 1

    lista_arco.append(arco_c)

input()