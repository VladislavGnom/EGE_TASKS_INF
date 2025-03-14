from itertools import *
from task_1 import check_table_cell

def get_solution(table: str, graph: str, letters_in_graph: str):
    for per in permutations(letters_in_graph):
        new_graph = table
        for i in range(1, 8):
            new_graph = new_graph.replace(str(i), per[i -1])
        
        if set(graph.split()) == set(new_graph.split()):
            return per
        
def get_answer(arr_table: list, map_iter: list | tuple, from_point, to_point):
    indx_start_elem = map_iter.index(from_point)
    indx_end_elem = map_iter.index(to_point)

    return int(arr_table[indx_start_elem][indx_end_elem])

def create_str_table_for_solution(array):
    table = ''
    for y, row in enumerate(array):
        for x, col in enumerate(row):
            if check_table_cell(col):
                pos = str(y + 1) + str(x + 1)
                table += pos + ' '

    table = table[:-1]    # delete end space
    return table

# array = [
#     ['*', '13', '', '', '', '2', ''],
#     ['13', '*', '', '30', '', '', '8'],
#     ['', '', '*', '3', '21', '5', ''],
#     ['', '30', '3', '*', '', '', '39'],
#     ['', '', '21', '', '*', '', '53'],
#     ['2', '', '5', '', '', '*', ''],
#     ['', '8', '', '39', '53', '', '*'],
# ]

# table = '12 16 21 24 27 34 35 36 42 43 47 53 57 61 63 72 74 75'
# graph = 'bd db de ed ea ae ca ac gc cg bg gb gf fg cf fc fe ef'
# letters_in_graph = 'abcdefg'

# result = get_solution(table, graph, letters_in_graph)
# print(get_answer(array, result, 'c', 'f'))
# print(get_answer(array, result, 'a', 'e'))
    