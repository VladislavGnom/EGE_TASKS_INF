from typing import Tuple


def check_table_cell(cell: str) -> bool:
    '''
    return True if cell have any logical value, and negative otherwise
    '''
    if cell.strip() == '*' or cell.strip() == '':
        return 0
    return 1


def create_help_table_from_array(arr: list) -> Tuple[Tuple[int, int]]:
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

def normilize_table(arr: list, help_arr: Tuple[Tuple[int, int]], line_indx1: int, line_indx2: int) -> list[list]:
    new_arr = arr.copy()
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


def shuffle_data_of_table(arr: list, number_of_cycles: int=1) -> list[list]:
    new_array = arr.copy()
    processed_lines_by_indexes = []
    pos = 0
    
    for _ in range(number_of_cycles):
        help_arr = create_help_table_from_array(new_array)    # create help table

        for i in range(1, len(arr)):
            cur = help_arr[pos]
            all_indx_keys = [el[0] for el in cur]
            if all_indx_keys.count(i) > 0: continue    # check first cond

            arr_line = help_arr[i]
            indx_arr_line = [el[0] for el in arr_line]
            if indx_arr_line.count(pos) > 0: continue    # check second cond

            if pos == i: continue    # clear self(repeating) values

            if pos in processed_lines_by_indexes: continue    # keep unique lines

            processed_lines_by_indexes.append(pos)
            new_array[pos], new_array[i] = new_array[i], new_array[pos]    # change lines
            new_array = normilize_table(new_array, help_arr, pos, i)
            break
        pos += 1

    return new_array


def print_beautiful_table(arr: list) -> None:
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

