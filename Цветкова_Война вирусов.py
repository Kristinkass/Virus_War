import tkinter as tk

def check_step(m, r, c,step):
    mas = [[0] * 12 for i in range(12)]
    k = 0
    p = 0
    for i in range(1, 11):
        for j in range(1, 11):
            mas[i][j] = m[k][p]
            if p < 9:
                p += 1
            else:
                p = 0
        if k < 9:
            k += 1
        else:
            k = 0
    row = r + 1
    col = c + 1
    if (mas[row - 1][col - 1] == step
            or mas[row - 1][col] == step
            or mas[row - 1][col + 1] == step
            or mas[row][col - 1] == step
            or mas[row][col + 1] == step
            or mas[row + 1][col - 1] == step
            or mas[row + 1][col] == step
            or mas[row + 1][col + 1] == step):
        return True
    return False

def start_the_game(menu): #стартовая функция, инициализирует игровое поле и обработчики событий, запускает игру и интерфейс.
    size_block = 46
    margin = 5
    FIELD_SIZE = 10
    screen = tk.Toplevel(menu)
    screen.title("Война вирусов")
    #screen.resizable(False, False)
    screen.geometry("1450x850")  #создает холст для рисования на экране игры.

    rules_summary = """
               За один ход комбинация из 3 действий: размножения или 
               уничтожения. Убитые крестики обводятся кружком, а 
               убитые нолики закрашиваются. 
               Цель игры – уничтожить все символы противника.
               Любые действия возможны только в доступных клетках, 
               которые расположены по соседству со своей собственной 
               клеткой.Можно пропустить полностью свой ход, но 
               запрещается выполнять этот ход частично.
               """
    rules_label = tk.Label(screen, text=rules_summary, bg='thistle3', font=('Helvetica', 16))
    rules_label.place(relx=0.42, rely=0.07)

    # Создаем холст для рисования
    canvas = tk.Canvas(screen, width=FIELD_SIZE * (size_block + margin) + margin,
                       height=FIELD_SIZE * (size_block + margin) + margin, bg='purple')
    canvas.pack()
    canvas.place(x=50, y=30)  # Измененное положение
    screen.focus_force()

    mas = [[0] * 10 for i in range(10)]
    query = 0  # счетчик хода
    step = 'x'
    step2 = 's'
    startX = True
    startO = True

    play_again_button = tk.Button(screen, text="Назад", width=12, bg='plum4', fg='white',
                               font=('Century', 25, 'bold'), command=screen.destroy)
    play_again_button.place(relx=0.15, rely=0.8)

    quit_button = tk.Button(screen, text="Выход", width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                         command=menu.destroy)
    quit_button.place(relx=0.6, rely=0.8)

    def on_click(event):  # процедура обработчика кликов по холсту, определяет действия при нажатии мыши на поле игры.
        nonlocal query, step, startX, startO, step2  # переменные для управления игровым процессом.
        col = event.x // (margin + size_block)
        row = event.y // (margin + size_block)

        if startX == True:
            if step == 'x' and col == 0 and row == 0:
                mas[row][col] = 'x'
                query += 1
                startX = False

        if startO == True:
            if step == 'o' and col == 9 and row == 9:
                mas[row][col] = 'o'
                query += 1
                startO = False

        if startX == False:
            if (step == 'x' and check_step(mas, row, col, step)) or (step2 == 's' and check_step(mas, row, col, step2)):
                if mas[row][col] == 0:  # пустая клетка
                    mas[row][col] = 'x'
                    query += 1
                if mas[row][col] == 'o':
                    mas[row][col] = 's'  # убитый o
                    query += 1

        if startO == False:
            if (step == 'o' and check_step(mas, row, col, step)) or (step2 == 'z' and check_step(mas, row, col, step2)):
                if mas[row][col] == 0:
                    (mas)[row][col] = 'o'
                    query += 1
                if mas[row][col] == 'x':
                    mas[row][col] = 'z'  # убитый x
                    query += 1

        if query == 3:  # проверяет количество сделанных ходов и меняет текущего игрока
            if step == 'x':
                step = 'o'
            elif step == 'o':
                step = 'x'
            if step2 == 's':
                step2 = 'z'
            elif step2 == 'z':
                step2 = 's'
            query = 0

        draw_board()

    def draw_board():
        canvas.delete("all")
        for row in range(10):
            for col in range(10):
                if mas[row][col] == 'x':
                    color = 'beige'
                elif mas[row][col] == 'o':
                    color = 'beige'
                elif mas[row][col] == 'z':
                    color = 'red'
                elif mas[row][col] == 's':
                    color = 'cornflowerblue'
                else:
                    color = 'white'
                x0 = col * size_block + (col + 1) * margin
                y0 = row * size_block + (row + 1) * margin
                x1 = x0 + size_block
                y1 = y0 + size_block
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')
                if color == 'beige':
                    if mas[row][col] == 'x' or mas[row][col] == 'z':
                        canvas.create_line(x0, y0, x1, y1, width=3, fill='cornflowerblue')
                        canvas.create_line(x1, y0, x0, y1, width=3, fill='cornflowerblue')
                    else:
                        canvas.create_oval(x0 + size_block // 2 - size_block // 4,
                                           y0 + size_block // 2 - size_block // 4,
                                           x1 - size_block // 2 + size_block // 4,
                                           y1 - size_block // 2 + size_block // 4,
                                           width=3, outline='red')


    canvas.bind("<Button-1>", on_click)
    draw_board()
    #menu.withdraw()  # Скрываем окно меню
    #screen.protocol("WM_DELETE_WINDOW", lambda: close_game(screen, menu))

def show_rules():
    rules_window = tk.Toplevel()
    rules_window.title("Правила игры")
    rules_window.geometry("1450x850")

    rules_window.image = tk.PhotoImage(file='Fon2_out.png')
    bg_logo = tk.Label(rules_window, image=rules_window.image)
    bg_logo.place(x=0, y=0, relwidth=1, relheight=1)
    rules_window.resizable(False, False)

    rules_text = """
    Правила игры:
    Данная игра рассчитана на двух игроков, которая проходит на игровом поле
    размером 10 на 10 клеток. Обозначениями становятся «крестик» и «нолик»,
    обозначающие символы каждого из игроков. 
    Начало игры происходит из противоположных углов игрового поля. 
    За один ход каждый из игроков может выполнить на выбор любую комбинацию из 3 действий: 
    размножение – игрок ставит один свой символ в незанятую клетку, соседнюю со своим символом; 
    уничтожение – игрок заражает символ противника, который находится рядом с клеткой, 
    занятой символом игрока. Зараженные клетки крестика становятся красными и переходят 
    в подчинение кружкам, а зараженные нолики – синим и переходят в подчинение крестикам. 
    Цель игры – заразить все символы противника.
    Любые действия возможно только в доступных для игрока клетках, то есть в тех, 
    которые расположены "по соседству" со своей собственной клеткой!
    Игра заканчивается, когда один игрок заражение все символы противника или 
    если отсутствует допустимый ход у игроков. 
    Побеждает тот, кто уничтожает все символы противника. 
    Если это не удаётся ни одному из игроков, то игра заканчивается вничью.
    """

    rules_label = tk.Label(rules_window, text=rules_text,bg='thistle3', font=("Helvetica", 16))
    rules_label.pack(pady=20)

    return_button = tk.Button(rules_window, text="Назад", width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'), command=rules_window.destroy)
    return_button.place(relx=0.5, rely=0.88, anchor="c")

def close_game(game_screen, menu):
    game_screen.destroy()
    menu.deiconify()  # Восстанавливаем окно меню
def open_menu():
    global start_the_game  # Скрываем главное окн0
    menu = tk.Tk()
    menu.title("Меню игры")
    menu.geometry("1450x850")
    menu.image = tk.PhotoImage(file='Fon2_out.png')
    bg_logo = tk.Label(menu, image=menu.image)
    bg_logo.place(x=0, y=0, relwidth=1, relheight=1)
    menu.resizable(False, False)
    play_button = tk.Button(menu, text='Играть', width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                      command=lambda: start_the_game(menu))
    play_button.place(relx=0.5, rely=0.45, anchor= "c")

    btn_rules = tk.Button(menu, text='Правила', width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                       command=show_rules)
    btn_rules.place(relx=0.5, rely=0.625, anchor="c")

    exit_button = tk.Button(menu, text='Выход', width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                        command=menu.destroy)
    exit_button.place(relx=0.5, rely=0.8, anchor= "c")
    menu.mainloop()

open_menu()

