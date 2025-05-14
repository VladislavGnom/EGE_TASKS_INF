import threading
import tkinter as tk
from tkinter import ttk
from random import randint
from copy import deepcopy

from solution_1 import get_solution, get_answer, create_str_table_for_solution
from task_1 import shuffle_data_of_table, print_beautiful_table, replace_numbers_in_table

NUMBER_OF_VARIANTS = 10    # количество вариантов задания
GRAPH = 'bd db de ed ea ae ca ac gc cg bg gb gf fg cf fc fe ef'    # все связи с таблицы
LETTERS_IN_GRAPH = 'abcdefg'    # все названия пунктов(каждый пункт - одна буква)

ARRAY_GLOBAL = []


def main():
    ARRAY = ARRAY_GLOBAL

    output = []

    for _ in range(NUMBER_OF_VARIANTS):
        variant = []

        new_array = deepcopy(ARRAY)
        new_array = replace_numbers_in_table(new_array, 1, 100)    # change numbers into array
        number_of_cycles = randint(1, len(new_array))    # параметр - глубина перемешки

        # formatted_arr - for frontend to display
        # result_array - for get answer (array similar with source array)
        result_array, formatted_arr = shuffle_data_of_table(new_array, number_of_cycles=number_of_cycles)    # create new updated array

        table = create_str_table_for_solution(result_array)    # create new help table
        result = get_solution(table, GRAPH, LETTERS_IN_GRAPH)    # get result of task

        # ----------- VALIDATE ANSWER BLOCK --------------------
        answer = get_answer(result_array, result, 'c', 'f') + get_answer(result_array, result, 'a', 'e')
        
        # ----------- END VALIDATE ANSWER BLOCK -----------

        variant.append(formatted_arr)    
        variant.append(answer)
        output.append(variant)

    # print_beautiful_table(output)
    print(output)


def create_table():
    try:
        size = int(size_entry.get())
    except ValueError:
        result_label.config(text="Ошибка: введите целое число!")
        return

    if size <= 0:
        result_label.config(text="Ошибка: размер должен быть > 0!")
        return

    # Очищаем предыдущую таблицу
    for widget in table_frame.winfo_children():
        widget.destroy()

    global entries
    entries = []
    for i in range(size):
        row_entries = []
        for j in range(size):
            if j > i:  # Верхний треугольник - editable
                entry = ttk.Entry(table_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.bind('<FocusOut>', lambda e, row=i, col=j: mirror_value(row, col))
            elif i == j:  # Диагональ - '*'
                entry = ttk.Entry(table_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, '*')  # Сначала вставляем значение
                entry.config(state='readonly')  # Затем делаем readonly
            else:  # Нижний треугольник - readonly
                entry = ttk.Entry(table_frame, width=5, state='readonly')
                entry.grid(row=i, column=j, padx=2, pady=2)
            row_entries.append(entry)
        entries.append(row_entries)
    result_label.config(text=f"Симметричная таблица {size}x{size} создана!")
    submit_button.config(state=tk.NORMAL)

def mirror_value(row, col):
    """Зеркалирует значение из верхнего треугольника в нижний"""
    if col > row:  # Проверяем, что это действительно верхний треугольник
        value = entries[row][col].get()
        entries[col][row].config(state='normal')
        entries[col][row].delete(0, tk.END)
        entries[col][row].insert(0, value)
        entries[col][row].config(state='readonly')

def submit_data():
    def send_to_server():
        global ARRAY_GLOBAL
        ARRAY_GLOBAL = []
        for i in range(len(entries)):
            row_data = []
            for j in range(len(entries[i])):
                row_data.append(entries[i][j].get())
            ARRAY_GLOBAL.append(row_data)
        
        result_label.config(text="Таблица отправлена!")
        main()    # выполняем генерацию заданий
    
    # Запускаем в отдельном потоке, чтобы не блокировать GUI
    threading.Thread(target=send_to_server, daemon=True).start()

# Создаем основное окно
root = tk.Tk()
root.title("Симметричная таблица")

# Фрейм для ввода размера
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)

ttk.Label(input_frame, text="Размер таблицы (n x n):").grid(row=0, column=0, sticky=tk.W)
size_entry = ttk.Entry(input_frame)
size_entry.grid(row=0, column=1, padx=5, pady=5)

# Кнопка создания таблицы
create_button = ttk.Button(input_frame, text="Создать симметричную таблицу", command=create_table)
create_button.grid(row=1, column=0, columnspan=2, pady=10)

# Фрейм для таблицы
table_frame = ttk.Frame(root, padding="10")
table_frame.pack(fill=tk.BOTH, expand=True)

# Кнопка отправки данных
submit_button = ttk.Button(root, text="Отправить данные", command=submit_data, state=tk.DISABLED)
submit_button.pack(pady=10)

# Метка для вывода результата
result_label = ttk.Label(root, text="")
result_label.pack()

root.mainloop()
