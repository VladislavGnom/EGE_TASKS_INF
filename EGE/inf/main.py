from random import randint
from copy import deepcopy

from solution_1 import get_solution, get_answer, create_str_table_for_solution
from task_1 import shuffle_data_of_table, print_beautiful_table, replace_numbers_in_table

NUMBER_OF_VARIANTS = 25

ARRAY = [
    ['*', '13', '', '', '', '2', ''],
    ['13', '*', '', '30', '', '', '8'],
    ['', '', '*', '3', '21', '5', ''],
    ['', '30', '3', '*', '', '', '39'],
    ['', '', '21', '', '*', '', '53'],
    ['2', '', '5', '', '', '*', ''],
    ['', '8', '', '39', '53', '', '*'],
]

graph = 'bd db de ed ea ae ca ac gc cg bg gb gf fg cf fc fe ef'
letters_in_graph = 'abcdefg'

output = []

for _ in range(NUMBER_OF_VARIANTS):
    variant = []

    new_array = deepcopy(ARRAY)
    new_array = replace_numbers_in_table(new_array, 1, 100)    # change numbers into array
    number_of_cycles = randint(1, len(new_array))

    # formatted_arr - for frontend to display
    # result_array - for get answer (array similar with source array)
    result_array, formatted_arr = shuffle_data_of_table(new_array, number_of_cycles=number_of_cycles)    # create new updated array

    table = create_str_table_for_solution(result_array)    # create new help table
    result = get_solution(table, graph, letters_in_graph)    # get result of task

    answer = get_answer(result_array, result, 'c', 'f') + get_answer(result_array, result, 'a', 'e')

    variant.append(formatted_arr)
    variant.append(answer)
    # get_answer(result_array, result, 'c', 'f')
    # get_answer(result_array, result, 'a', 'e')
    # print_beautiful_table(result_array)
    output.append(variant)

# print_beautiful_table(output)
print(output)

