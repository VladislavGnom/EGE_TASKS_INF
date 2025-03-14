import tkinter as tk

from random import randint
from typing import Tuple
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


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
    res_arr = arr.copy()
    line1, line2 = help_arr[line_indx1], help_arr[line_indx2]

    for indx1, num1 in line1:
        if res_arr[indx1][line_indx1] == str(num1):
            res_arr[indx1][line_indx1] = ''
        res_arr[indx1][line_indx2] = str(num1)
    
    for indx2, num2 in line2:
        if res_arr[indx2][line_indx2] == str(num2):
            res_arr[indx2][line_indx2] = ''
        res_arr[indx2][line_indx1] = str(num2)

    # '*' - normilize
    for indx, row in enumerate(res_arr):
        new_row = [el if el != '*' else '' for el in row]
        new_row = [el if indx_el != indx else '*' for indx_el, el in enumerate(new_row)]
        res_arr[indx] = new_row

    return res_arr


def shuffle_data_of_table(arr: list=None, number_of_cycles: int=1) -> list[list]:
    is_from_gui = False
    if arr is None:
        is_from_gui = True

        try:
            arr = eval(source_table_tf.get('1.0', END))
        except Exception as error:
            result.delete('1.0', END)
            result.insert(END, 'Ошибка! Это неверная таблица!')
            return 
        
        try:
            count_of_cycles = int(check_number_of_cycle_var.get())
            number_of_cycles = count_of_cycles if isinstance(count_of_cycles, int) else number_of_cycles

            if not(1 <= number_of_cycles <= len(arr)): 
                raise Exception('Ошибка! Число лежит в неподдерживаемом диапазоне')
        except Exception as error:
            result.delete('1.0', END)
            result.insert(END, 'Ошибка! Неверное число!')
            return 

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

    if is_from_gui:
        result.delete('1.0', END)
        result.insert(END, '[\n')
        for row in new_array:
            result.insert(END, f"{' ' * 4}{[row[i] for i in range(len(row))]}\n")
        result.insert(END, ']')

    formatted_arr = []

    for row in new_array:
        text_row = ''
        for ch in row:
            if ch == '':
                text_row += ' '
            else:
                text_row += ch
            text_row += '_'
        formatted_arr.append(text_row)

    return (new_array, formatted_arr)


def print_beautiful_table(arr: list) -> None:
    for row in arr:
        print(row)

def check_condition_for_numbers_in_table(arr: list):
    numbers_count = {}

    for row in arr:
        for col in row:
            if not check_table_cell(col): continue

            numbers_count[col] = numbers_count.get(col, 0) + 1
    # print(f'{numbers_count=}')
    # print_beautiful_table(arr)
    return numbers_count

def replace_numbers_in_table(arr, min_num=1, max_num=100):
    new_arr = arr.copy()
    numbers_replace = {}
    # print(check_condition_for_numbers_in_table(new_arr))

    for y, row in enumerate(new_arr):
        for x, col in enumerate(row):
            if not check_table_cell(col): continue

            if col not in numbers_replace.keys():
                rand_num = str(randint(min_num, max_num))

                while not(check_condition_for_numbers_in_table(new_arr).get(rand_num, 0) == 0):
                    # print(check_condition_for_numbers_in_table(new_arr).get(rand_num, 0))
                    rand_num = str(randint(min_num, max_num))

                numbers_replace[col] = rand_num

            new_arr[y][x] = numbers_replace[col]

    return new_arr


array = [
    ['*', '13', '', '', '', '2', ''],
    ['13', '*', '', '30', '', '', '8'],
    ['', '', '*', '3', '21', '5', ''],
    ['', '30', '3', '*', '', '', '39'],
    ['', '', '21', '', '*', '', '53'],
    ['2', '', '5', '', '', '*', ''],
    ['', '8', '', '39', '53', '', '*'],
]

def main():
    # GUI
    # ------------------------------------------------------
    window = Tk()
    window.title('Генерация изменённого задания №1 ЕГЭ ИКТ')
    window.geometry('400x520')

    frame = Frame(
    window,
    padx = 10,
    pady = 10
    )
    frame.pack(expand=True)


    source_table_lb = Label(
    frame,
    text='Вставьте свою таблицу: '
    )
    source_table_lb.grid(row=1, column=1)

    source_table_tf = ScrolledText(frame, width=45,  height=10)
    source_table_tf.grid(row=2, column=1)

    check_number_of_cycle_var_lb = tk.Label(frame, text="Введите число - качество перемешки: ")
    check_number_of_cycle_var_lb.grid(row=3, column=1, pady=5)

    check_number_of_cycle_var = Entry(frame)
    check_number_of_cycle_var.grid(row=4, column=1)

    cal_btn = Button(
    frame,
    text='Сгенерировать таблицу',
    command=shuffle_data_of_table
    )
    cal_btn.grid(row=5, column=1, pady=5)


    result_lb = Label(
    frame,
    text='Результат: '
    )
    result_lb.grid(row=6, column=1)

    result = ScrolledText(
        frame, 
        width=45,  
        height=10
    )
    result.grid(row=7, column=1)



    window.mainloop()
    # ------------------------------------------------------
# print_beautiful_table(shuffle_data_of_table(array, number_of_cycles=4))

if __name__ == '__main__':
    main()
