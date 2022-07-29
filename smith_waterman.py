# algoritmo de alinhamento
# smith waterman

# entrada
s1 = "TGGT"
s2 = "CGT"
gap = -3
match = 2
mismatch = -1

# process in
s1 = "U" + s1

s2 = "U" + s2


class node:
    def __init__(self, value, n1, n2):
        self.value = value
        self.n1 = n1
        self.n2 = n2
        self.op = ""


matrix = [list([node(0, s1[i], s2[j]) for i in range(len(s1))])
          for j in range(len(s2))]

for j in range(len(s2)):
    matrix[j][0].value = gap * j

for i in range(len(s1)):
    matrix[0][i].value = gap * i

# for j in range(len(s2)):
#     for i in range(len(s1)):
#         print(matrix[j][i].value, end=' ')
#     print("\n")

# print("========================================")


def set_value(matrix, act_node, gap, mismatch, match):
    n1 = [act_node[0]][act_node[1]]
    n2 = matrix[act_node[0]][act_node[1]]
    if n1 == n2:
        match = matrix[act_node[0]-1][act_node[1]-1].value + match
    else:
        mismatch = matrix[act_node[0]-1][act_node[1]-1].value + mismatch

    gap_left = matrix[act_node[0]][act_node[1]-1].value + gap

    gap_top = matrix[act_node[0]-1][act_node[1]].value + gap

    dict_value = {"match": match, "mismatch": mismatch,
                  "gap_left": gap_left, "gap_top": gap_top}

    # print(dict_value)

    matrix[act_node[0]][act_node[1]].op = max(dict_value)

    matrix[act_node[0]][act_node[1]].value = dict_value[max(dict_value)]


for j in range(len(s2)-1):
    for i in range(len(s1)-1):
        set_value(matrix, (j+1, i+1), gap, mismatch, match)

for j in range(len(s2)):
    for i in range(len(s1)):
        print(matrix[j][i].value, end=' ')
    print("\n")

# BACKTRACE
act_node = [len(s2)-1, len(s1)-1]

seq_s1 = ""
seq_s2 = ""

seq_s1 = seq_s1 + matrix[act_node[0]][act_node[1]].n1
seq_s2 = seq_s2 + matrix[act_node[0]][act_node[1]].n2

while(True):
    if matrix[act_node[0]][act_node[1]].op == "match":
        act_node[0] = act_node[0] - 1
        act_node[1] = act_node[1] - 1
        seq_s1 = seq_s1 + matrix[act_node[0]][act_node[1]].n1
        seq_s2 = seq_s2 + matrix[act_node[0]][act_node[1]].n2
    elif matrix[act_node[0]][act_node[1]].op == "mismatch":
        act_node[0] = act_node[0] - 1
        act_node[1] = act_node[1] - 1
        seq_s1 = seq_s1 + matrix[act_node[0]][act_node[1]].n1
        seq_s2 = seq_s2 + matrix[act_node[0]][act_node[1]].n2
    elif matrix[act_node[0]][act_node[1]].op == "gap_left":
        act_node[0] = act_node[0] - 1
        seq_s1 = seq_s1 + "-"
        seq_s2 = seq_s2 + matrix[act_node[0]][act_node[1]].n2
    elif matrix[act_node[0]][act_node[1]].op == "gap_top":
        act_node[1] = act_node[1] - 1
        seq_s1 = seq_s1 + matrix[act_node[0]][act_node[1]].n1
        seq_s2 = seq_s2 + "-"
    else:
        break
