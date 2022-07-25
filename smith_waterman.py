# algoritmo de alinhamento
# smith waterman

# entrada
s1 = "TGGT"
s2 = "CGT"
gap = 0
match = 0
mismatch = 0

# process in
s1 = s1 + "U"
s2 = s2 + "U"


class node:
    c_from = []

    def __init__(self, value):
        self.value = value


matrix = [list([node(0) for i in range(len(s1))]) for j in range(len(s2))]

for i in range(len(s2)):
    matrix[i][0].value = gap*i

matrix[0] = [node(gap*i) for i in range(len(s1))]


def set_value(c_node, left, diagonal, bottom, gap, match, mismatch, i, j, n1, n2):

    left = left.value+gap

    if n1 == n2:
        diagonal = diagonal.value+match
    else:
        diagonal = diagonal.value+mismatch

    bottom = bottom.value + gap

    value_list = [left, diagonal, bottom]

    value_list.sort()

    value = value_list[-1]

    c_node.value = value

    # link node
    if value == left:
        c_node.c_from.append((i, j+1))
    if value == diagonal:
        c_node.c_from.append((i+1, j+1))
    if value == bottom:
        c_node.c_from.append((i+1, j))


for i in range(len(s2)-1):
    for j in range(len(s1)-1):
        set_value(matrix[i+1][j+1], matrix[i][j+1], matrix[i][j],
                  matrix[i+1][j], gap, match, mismatch, i, j, s1[j], s2[i])

# process out
seq_alinhada_s1 = ""
seq_alinhada_s2 = ""

# do canto superior direito
i = len(s2)-1
j = len(s1)-1
act_node = matrix[i][j]

while(len(act_node.c_from) != 0):
    seq_alinhada_s1 = seq_alinhada_s1+s1[i]
    seq_alinhada_s2 = seq_alinhada_s2+s2[j]

    i = act_node.c_from[0][0]
    j = act_node.c_from[0][1]

    act_node = matrix[i][j]

# correcao
if i != 0 and j != 0:

    exit
