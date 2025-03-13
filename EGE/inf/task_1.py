# import matplotlib.pyplot as plt
# import networkx as nx

# node_color=['black']

# G = nx.Graph()  # создаём объект графа

# # определяем список узлов (ID узлов)
# nodes = [1, 2, 3, 4, 5]

# # определяем список рёбер
# # список кортежей, каждый из которых представляет ребро
# # кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
# edges = [('a', 'b', 10), ('c', 'd', 10), ('c', 'a', 10)]

# # добавляем информацию в объект графа
# # G.add_nodes_from(nodes)
# G.add_weighted_edges_from(edges)

# # Позиции узлов (Spring Layout - автоматически расставляет)
# pos = nx.spring_layout(G, seed=10000)

# # рисуем граф и отображаем его
# nx.draw(G, with_labels=False, font_weight='bold', node_color=node_color, node_size=10)


# # Добавляем подписи рядом с вершинами (смещаем их вверх)
# labels = {node: node for node in G.nodes()}
# nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color="black", verticalalignment='center')

# plt.show()

# new code
from typing import Tuple


def check_table_cell(cell: str) -> bool:
    '''
    return True if cell have any logical value, and negative otherwise
    '''
    if cell.strip() == '*' or cell.strip() == '':
        return 0
    return 1


def create_help_table_form_array(arr) -> Tuple[Tuple[int, int]]:
    '''return tuple with tuples where first num is index of element in the table,
       second num is value by this index
    '''
    res = []

    for y, row in enumerate(arr):
        help_lst = []

        for x, col in enumerate(row):        
            if check_table_cell(col):
                index_of_element = x
                value = int(col)
                pair = (index_of_element, value)

                help_lst.append(pair)

        help_lst = tuple(help_lst)
        res.append(help_lst)

    return tuple(res)

def normilize_table(arr, help_arr, line_indx1, line_indx2):
    new_arr = arr.copy()
    # new_arr = [[0 for _ in range(7)] for _ in range(7)]
    line1, line2 = help_arr[line_indx1], help_arr[line_indx2]

    for indx1, num1 in line1:
        if new_arr[indx1][line_indx1] == str(num1):
            new_arr[indx1][line_indx1] = ''
        new_arr[indx1][line_indx2] = str(num1)
    
    for indx2, num2 in line2:
        if new_arr[indx2][line_indx2] == str(num2):
            new_arr[indx2][line_indx2] = ''
        new_arr[indx2][line_indx1] = str(num2)

    # '*' - normilize
    for indx, row in enumerate(new_arr):
        new_row = [el if el != '*' else '' for el in row]
        new_row = [el if indx_el != indx else '*' for indx_el, el in enumerate(new_row)]
        new_arr[indx] = new_row

    return new_arr


def shuffle_data_of_table(arr, number_of_cycles=1) -> list[list]:
    new_array = arr.copy()
    processed_lines_by_indexes = []
    pos = 0
    
    for _ in range(number_of_cycles):
        help_arr = create_help_table_form_array(new_array)    # create help table

        for i in range(1, len(arr)):
            cur = help_arr[pos]
            all_indx_keys = [el[0] for el in cur]
            if all_indx_keys.count(i) > 0: continue    # check first cond

            arr_line = help_arr[i]
            indx_arr_line = [el[0] for el in arr_line]
            if indx_arr_line.count(pos) > 0: continue    # check second cond

            if pos == i: continue    # clear self values

            if pos in processed_lines_by_indexes: continue    # keep unique lines

            processed_lines_by_indexes.append(pos)
            new_array[pos], new_array[i] = new_array[i], new_array[pos]    # change lines
            new_array = normilize_table(new_array, help_arr, pos, i)
            break
        pos += 1

        
    
    # for y, row in enumerate(help_arr):
    #     next_position = y + 1
    #     is_true = True
    #     for el in row:
    #         index_of_element, value = el
    #         if index_of_element == next_position: 
    #             is_true = False
    #             break


    return new_array


def print_beautiful_table(arr):
    for row in arr:
        print(row)


array = [
    ['*', '13', '', '', '', '2', ''],
    ['13', '*', '', '30', '', '', '8'],
    ['', '', '*', '3', '21', '5', ''],
    ['', '30', '3', '*', '', '', '39'],
    ['', '', '21', '', '*', '', '53'],
    ['2', '', '5', '', '', '*', ''],
    ['', '8', '', '39', '53', '', '*'],
]

print_beautiful_table(shuffle_data_of_table(array, number_of_cycles=4))

