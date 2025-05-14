from itertools import *
from task_1 import check_table_cell

def get_solution(table: str, graph: str, letters_in_graph: str, from_point=1, to_point=8):
    for per in permutations(letters_in_graph):
        new_graph = table
        for i in range(from_point, to_point):
            new_graph = new_graph.replace(str(i), per[i - 1])
        
        if set(graph.split()) == set(new_graph.split()):
            return per
        
def get_answer(arr_table: list, map_iter: list | tuple, from_point, to_point):
    """Получает длину маршрута из пункта from_point до to_point"""

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
