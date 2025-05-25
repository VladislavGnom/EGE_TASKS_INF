import threading
import tkinter as tk
from tkinter import ttk
from random import randint
from copy import deepcopy

from solution_1 import get_solution, get_answer, create_str_table_for_solution
from task_1 import shuffle_data_of_table, print_beautiful_table, replace_numbers_in_table

# NUMBER_OF_VARIANTS = 10    # количество вариантов задания
# GRAPH = 'ев ве вб бв гб бг ба аб да ад дв вд ед де'    # все связи с таблицы
# LETTERS_IN_GRAPH = 'абвгде'    # все названия пунктов(каждый пункт - одна буква)

ARRAY_GLOBAL = []

# 'ab ae af ba bc be cb cd ce dc df ea eb ec ef fa fd fe'
# gf fg ga ag ad da de ed ef fe ab ba bg gb bc cb cd dc
def make_answer_by_points(result_array, result, points) -> int:
    answer = 0
    for p1, p2 in points:
        answer += get_answer(result_array, result, p1, p2)
        
    return answer

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
        result = get_solution(table, GRAPH, LETTERS_IN_GRAPH, to_point=len(new_array) + 1)    # get result of task

        # ----------- VALIDATE ANSWER BLOCK --------------------
        answer = make_answer_by_points(result_array, result, ARRAY_LINK_ANSWERS)
        
        # ----------- END VALIDATE ANSWER BLOCK -----------

        variant.append(formatted_arr)    
        variant.append(answer)
        output.append(variant)

    # print_beautiful_table(output)
    print(output)

def normilize_size_data(raw_links_data):
    letters = [ch for ch in set(links_entry.get()) if ch.isalpha()]
    size = len(letters)

    return letters, size

def create_table():
    try:
        size = normilize_size_data(links_entry.get())[1]
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

    global NUMBER_OF_VARIANTS, LETTERS_IN_GRAPH, GRAPH
    NUMBER_OF_VARIANTS = int(number_of_variants_entry.get())
    LETTERS_IN_GRAPH = normilize_size_data(links_entry.get())[0]
    GRAPH = links_entry.get().replace("'", '')

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

        global ARRAY_LINK_ANSWERS
        ARRAY_LINK_ANSWERS = []
        for i in range(len(field_entries)):
            row_data = []
            for j in range(2):
                row_data.append(field_entries[i][j].get())
            ARRAY_LINK_ANSWERS.append(row_data)

        main()    # выполняем генерацию заданий
    
    # Запускаем в отдельном потоке, чтобы не блокировать GUI
    threading.Thread(target=send_to_server, daemon=True).start()

def create_fields():
    try:
        number_of_fields = int(input_count_entry.get())
    except ValueError:
        result_label.config(text="Ошибка: введите целое число!")
        return
    
    # Очищаем предыдущую разметку
    for widget in field_frame.winfo_children():
        widget.destroy()

    global field_entries
    field_entries = []
    for i in range(number_of_fields):
        label = ttk.Label(field_frame, text="Между пунктами:")
        entry1 = ttk.Entry(field_frame, width=5)
        entry2 = ttk.Entry(field_frame, width=5)
        label.grid(row=i, column=0, padx=2, pady=2)
        entry1.grid(row=i, column=1, padx=2, pady=2)
        entry2.grid(row=i, column=2, padx=2, pady=2)
        row_entries = [entry1, entry2]
        field_entries.append(row_entries)    

    result_label.config(text=f"Поля для ввода пунктов созданы!")

# Создаем основное окно
root = tk.Tk()
root.title("Симметричная таблица")

# Фрейм для ввода соотношений полей
input_fields_frame = ttk.Frame(root, padding="10")
input_fields_frame.pack(fill=tk.X)

ttk.Label(input_fields_frame, text="Связи пунктов:").grid(row=0, column=0, sticky=tk.W)
links_entry = ttk.Entry(input_fields_frame)
links_entry.grid(row=0, column=1, padx=5, pady=5)

# Фрейм для ввода размера
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)

ttk.Label(input_frame, text="Количество вариантов: ").grid(row=1, column=0, sticky=tk.W)
number_of_variants_entry = ttk.Entry(input_frame)
number_of_variants_entry.grid(row=1, column=1, padx=5, pady=5)


# Кнопка создания таблицы
create_button = ttk.Button(input_frame, text="Создать симметричную таблицу", command=create_table)
create_button.grid(row=2, column=0, columnspan=2, pady=10)

# Фрейм для таблицы
table_frame = ttk.Frame(root, padding="10")
table_frame.pack(fill=tk.BOTH, expand=True)

# Фрейм для ввода количества растояний между пунктов для ответа
input_count_frame = ttk.Frame(root, padding="10")
input_count_frame.pack(fill=tk.X)

ttk.Label(input_count_frame, text="Количество расстояний: ").grid(row=2, column=0, sticky=tk.W)
input_count_entry = ttk.Entry(input_count_frame)
input_count_entry.grid(row=2, column=1, padx=5, pady=5)

# Фрейм для ввода пунктов
field_frame = ttk.Frame(root, padding="10")
field_frame.pack(fill=tk.BOTH, expand=True)

# Кнопка создания полей для ввода пунктов
create_way_button = ttk.Button(root, text="Создать поля", command=create_fields)
create_way_button.pack(pady=10)

# Кнопка отправки данных
submit_button = ttk.Button(root, text="Отправить данные", command=submit_data, state=tk.DISABLED)
submit_button.pack(pady=10)

# Метка для вывода результата
result_label = ttk.Label(root, text="")
result_label.pack()

root.mainloop()
