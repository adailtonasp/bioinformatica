# algoritmo de alinhamento
# smith waterman
import csv
import sys


class node:
    def __init__(self, value, n1, n2):
        self.value = value
        self.n1 = n1
        self.n2 = n2
        self.op = ""


def create_matrix(s1, s2, gap):

    s1 = "-" + s1

    s2 = "-" + s2

    matrix = [list([node(0, s1[i], s2[j]) for i in range(len(s1))])
              for j in range(len(s2))]

    for j in range(len(s2)):
        matrix[j][0].value = gap * j

    for i in range(len(s1)):
        matrix[0][i].value = gap * i

    return matrix


def set_value(matrix, act_node, gap, mismatch, match):
    # act_node => (i, j)
    # i relativo a coluna
    # j relativo a linha
    # o primeiro indice da matrix precisa ser o iterador da linha
    # o segundo indice sera o iterador da coluna
    n1 = matrix[act_node[1]][act_node[0]].n1
    n2 = matrix[act_node[1]][act_node[0]].n2

    gap_left = matrix[act_node[1]][act_node[0]-1].value + gap

    gap_top = matrix[act_node[1]-1][act_node[0]].value + gap

    dict_value = {"gap_left": gap_left, "gap_top": gap_top}

    if n1 == n2:
        match = matrix[act_node[1]-1][act_node[0]-1].value + match
        dict_value.setdefault("match", match)
    else:
        mismatch = matrix[act_node[1]-1][act_node[0]-1].value + mismatch
        dict_value.setdefault("mismatch", mismatch)

    # adicionar os demais valores com o mesmo valor maximo

    value = sorted(dict_value.items(), key=lambda x: x[1])[-1]

    matrix[act_node[1]][act_node[0]].op = value[0]

    matrix[act_node[1]][act_node[0]].value = value[1]


def backtrace(matrix):
    # max_value_coluna = matrix[len(matrix)-1][0].value
    # index_i = 0
    # for i in range(1, len(matrix[0])):
    #     if matrix[len(matrix)-1][i].value >= max_value_coluna:
    #         max_value_coluna = matrix[len(matrix)-1][i].value
    #         index_i = i

    # max_value_linha = matrix[len(matrix)-1][0].value
    # index_j = 0
    # for j in range(1, len(matrix)):
    #     if matrix[j][len(matrix[0])-1].value >= max_value_linha:
    #         max_value_linha = matrix[j][len(matrix[0])-1].value
    #         index_j = j

    # if max_value_coluna > max_value_linha:
    #     act_node = [index_i, len(matrix)-1]
    # elif max_value_coluna < max_value_linha:
    #     act_node = [len(matrix[0])-1, index_j]
    # else:
    #     act_node = [len(matrix[0])-1, len(matrix)-1]

    act_node = [len(matrix[0])-1, len(matrix)-1]

    seq_s1 = ""
    seq_s2 = ""

    # seq_s1 = seq_s1 + matrix[act_node[1]][act_node[0]].n1
    # seq_s2 = seq_s2 + matrix[act_node[1]][act_node[0]].n2

    while(True):
        if(matrix[act_node[1]][act_node[0]].value == 0):
            break
        if matrix[act_node[1]][act_node[0]].op == "match":
            act_node[0] = act_node[0] - 1
            act_node[1] = act_node[1] - 1
            seq_s1 = seq_s1 + matrix[act_node[1]+1][act_node[0]+1].n1
            seq_s2 = seq_s2 + matrix[act_node[1]+1][act_node[0]+1].n2
        elif matrix[act_node[1]][act_node[0]].op == "mismatch":
            act_node[0] = act_node[0] - 1
            act_node[1] = act_node[1] - 1
            seq_s1 = seq_s1 + matrix[act_node[1]+1][act_node[0]+1].n1
            seq_s2 = seq_s2 + matrix[act_node[1]+1][act_node[0]+1].n2
        elif matrix[act_node[1]][act_node[0]].op == "gap_left":
            act_node[0] = act_node[0] - 1
            seq_s2 = seq_s2 + matrix[act_node[1]][act_node[0]+1].n2
            seq_s1 = seq_s1 + "-"
        elif matrix[act_node[1]][act_node[0]].op == "gap_top":
            act_node[1] = act_node[1] - 1
            seq_s2 = seq_s2 + "-"
            seq_s1 = seq_s1 + matrix[act_node[1]+1][act_node[0]].n1
        else:
            break

    print("seq_s1", seq_s1)
    print("seq_s2", seq_s2)
    print("act_node", act_node)

    return seq_s1, seq_s2, act_node


def correct_backtrace(matrix, act_node, seq_s1, seq_s2):
    if act_node[0] == 0 and act_node[1] > 0:  # siginica que esta na primeira coluna
        for i in range(act_node[1], 1):
            seq_s2 = seq_s2 + matrix[i-1][act_node[0]].n2
            seq_s1 = seq_s1 + "-"
    if act_node[1] == 0 and act_node[0] > 0:
        for j in range(act_node[0], 1):  # significa que esta na primeira linha
            seq_s1 = seq_s1 + matrix[act_node[1]][j-1].n1
            seq_s2 = seq_s2 + "-"


def calc_backtrace_value(matrix, seq_s1, seq_s2, match, mismatch, gap):

    act_node = [len(matrix[0])-1, len(matrix)-1]

    meta_value = matrix[act_node[1]][act_node[0]].value

    sum_value = 0

    for i in range(len(seq_s1)):
        if seq_s1[i] == "-" and seq_s2[i] == "-":
            sum_value = sum_value
            print("Double Gap")
        elif seq_s1[i] == "-" or seq_s2[i] == "-":
            sum_value = sum_value + gap
        elif seq_s1[i] != seq_s2[i]:
            sum_value = sum_value + mismatch
        else:  # if seq_s1[i] == seq_s2[i]:
            sum_value = sum_value + match

    print("meta_value", meta_value)
    print("sum_value", sum_value)


def main():

    with open(sys.argv[2], 'w') as file_w:
        file_w.write("")

    with open(sys.argv[1], 'r') as file_r:
        content_r = csv.reader(file_r, delimiter=";")
        s1 = "CGGUACAUUGUUGCAGGCAAUUGUGAGUUGUGUUAGACAUGGGCAGUUUAACCCUGGGAGGGGCUGGUGGUUUACCUGACUACUUAUUGCGCUUUGGCGGGGCUGCAGCCUAGCUGGUCCCCGUGCGAUUUCC"
        s2 = "CGGUACAUUGUUGCAGGCAAUUGUGAAGUGAGUUAGACAUGGGCAGUUUAACCCUGGUGGGGUGGUUUACCUGACUGUACUACUUAUUGCGCUUUGGCUGCAGCUGGUCCCCUCCCCGUGCGAUUUCCCUUCAACGCAUGGUAGUGGGAACCUGUUGGAGAGGUUCUGAUGAAACUAACCCUGACAUGUUACUGGGCUGG"

        gap = -2
        match = 3
        mismatch = -3

        matrix = create_matrix(s1, s2, gap)

        for j in range(len(matrix)-1):  # itera sobre linha
            for i in range(len(matrix[0])-1):  # itera sobre coluna
                set_value(matrix, (i+1, j+1), gap, mismatch, match)

        for j in range(len(matrix)):
            for i in range(len(matrix[0])):
                print(matrix[j][i].value, end=' ')
            print("\n")

        seq_s1, seq_s2, act_node = backtrace(matrix)

        calc_backtrace_value(matrix, seq_s1, seq_s2, match, mismatch, gap)


if __name__ == "__main__":
    main()
