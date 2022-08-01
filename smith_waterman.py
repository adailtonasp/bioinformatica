# algoritmo de alinhamento
# smith waterman

# entrada

s2 = "GUGGGCUGGAAGCAGCGACGGCUGGAAGGAUUGAACCACACCGACGCGAGAAGCCUACCUGAACUGGUAUUGGUUGAUUCGUUUAUGCCAACAUCGCGGCUCUUCUCUUAUCCGCCGAUUAUCGCAGAAGCCGCUCGGGCUGUUUCUCUUCUGCCCGGGUGAAGUCUCAGGGGUGCACACCACAUCUGAUCUCUUUACAA"
s1 = "GUGGAAGCAGCGACGUGACGGCUGGAAGGAUUGAACCGACGCGAGAAGCCUACCUGAACUGGUAUUGGUUGACUUGAUUCGUUUAUGCCAACAUCGCGGCUCUUAUUCUAACCUAUCCGCCGAUUAUCGCAGA"

gap = -3
match = 1
mismatch = -1

# process in
s1 = "-" + s1

s2 = "-" + s2


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
    n1 = matrix[act_node[0]][act_node[1]].n1
    n2 = matrix[act_node[0]][act_node[1]].n2

    gap_left = matrix[act_node[0]][act_node[1]-1].value + gap

    gap_top = matrix[act_node[0]-1][act_node[1]].value + gap

    dict_value = {"gap_left": gap_left, "gap_top": gap_top}

    if n1 == n2:
        match = matrix[act_node[0]-1][act_node[1]-1].value + match
        dict_value.setdefault("match",match)
        #dict_value["match"] = match
    else:
        mismatch = matrix[act_node[0]-1][act_node[1]-1].value + mismatch
        dict_value.setdefault("mismatch",mismatch)
        #dict_value["mismatch"] = mismatch

    # print(dict_value)

    value = sorted(dict_value.items(),key=lambda x:x[1])[-1]

    #value = max(dict_value)

    matrix[act_node[0]][act_node[1]].op = value[0]

    matrix[act_node[0]][act_node[1]].value = value[1]


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

#CORRECAO
if act_node[0] == 0 : #siginica que esta na primeira coluna
    for i in range(act_node[1]):
        seq_s2 = seq_s2 + matrix[act_node[0]][i].n1
        seq_s1 = seq_s1 + "-"
elif act_node[1] == 0:
    for j in range(act_node[0],0):
        seq_s1 = seq_s1 + matrix[j][act_node[j]].n1
        seq_s2 = seq_s2 + "-"

print(seq_s1+"\n")
print(seq_s2+"\n")

act_node = [len(s2)-1, len(s1)-1]

meta_value = matrix[act_node[0]][act_node[1]].value

sum_value = 0
for i in range(len(seq_s1)):
    if seq_s1[i] == "-" and seq_s2[i] == "-":
        sum_value = sum_value
        print("Double Gap")
    elif seq_s1[i] == "-" or seq_s2[i] == "-":
        sum_value = sum_value  + gap
    elif seq_s1[i] != seq_s2[i]:
        sum_value = sum_value + mismatch
    else:
        sum_value = sum_value + match

print("meta_value",meta_value)
print("sum_value",sum_value)