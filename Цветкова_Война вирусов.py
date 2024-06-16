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
    screen.resizable(False, False)
    screen.geometry("1450x850+120+50")  #создает холст для рисования на экране игры.

    rules_summary = """
     За один ход комбинация из 3 действий: РАЗМНОЖЕНИЕ 
     или ЗАРАЖЕНИЕ. Зараженные клетки крестика становятся   
     красными и переходят в подчинение кружкам, а зараженные    
     нолики – синими и переходят в подчинение крестикам. 
     ЦЕЛЬ ИГРЫ – заразить все клетки с символом противника.
     Любые действия возможно только в ДОСТУПНЫХ для игрока 
     клетках, которые расположены "по соседству" от клеток
     игроков (x/o) или от зараженных, пподчиненных им!
     """
    rules_label = tk.Label(screen, text=rules_summary, bg='thistle3', font=('Helvetica', 16), justify="left")
    rules_label.place(relx=0.42, rely=0.18)

    # Создаем холст для рисования
    canvas = tk.Canvas(screen, width=FIELD_SIZE * (size_block + margin) + margin,
                       height=FIELD_SIZE * (size_block + margin) + margin, bg='purple')
    canvas.pack()
    canvas.place(x=50, y=60)  # Измененное положение
    screen.focus_force()

    mas = [[0] * 10 for i in range(10)]
    query = 0  # счетчик хода
    step = 'x'
    step2 = 's'
    startX = True
    startO = True

    # Кнопка "Назад"
    def back_to_menu():
        screen.destroy()

    play_return_button = tk.Button(screen, text="Назад", width=12, bg='plum4', fg='white',
                                   font=('Century', 25, 'bold'), command=back_to_menu)
    play_return_button.place(relx=0.05, rely=0.8)

    quit_button = tk.Button(screen, text="Выход", width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                            command=menu.destroy)
    quit_button.place(relx=0.71, rely=0.8)

    skip_button = tk.Button(screen, text="Пропуск хода", width=12, bg='plum4', fg='white',
                            font=('Century', 25, 'bold'), command=lambda: skip_turn())
    skip_button.place(relx=0.38, rely=0.8)

    # Обновляемый текст вверху
    turn_label = tk.Label(screen, text="Ходит игрок №1 |x|", bg="plum4", fg='white', font=('Century', 16, 'bold'))
    turn_label.pack(side="top", fill="x")

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
                    mas[row][col] = 's'  # зараженный o => колония x
                    query += 1
                    check_win(mas, step, step2)

        if startO == False:
            if (step == 'o' and check_step(mas, row, col, step)) or (step2 == 'z' and check_step(mas, row, col, step2)):
                if mas[row][col] == 0:
                    (mas)[row][col] = 'o'
                    query += 1
                if mas[row][col] == 'x':
                    mas[row][col] = 'z'  # зараженный x => колония o
                    query += 1
                    check_win(mas, step, step2)

        if query == 3:  # проверяет количество сделанных ходов и меняет текущего игрока
            if step == 'x' :
                step = 'o'
                turn_label.config(text="Ходит игрок №2 |o|")
            elif step == 'o':
                step = 'x'
                turn_label.config(text="Ходит игрок №1 |x|")
            if step2 == 's':
                step2 = 'z'
            elif step2 == 'z':
                step2 = 's'
            query = 0

        draw_board()

    def skip_turn():  # Функция для пропуска хода
        nonlocal query, step, step2, skip_button
        if query < 3:
            if step == 'x':
                step = 'o'
                turn_label.config(text="Ходит игрок №2 |o|")
            elif step == 'o':
                step = 'x'
                turn_label.config(text="Ходит игрок №1 |x|")
            if step2 == 's':
                step2 = 'z'
            elif step2 == 'z':
                step2 = 's'
            query = 0
            draw_board()
            on_click
            return

    def check_win(mas, current_step, current_step2):
        nonlocal step, step2
        if all(cell != 0 for row in mas for cell in row) or all(cell != 'x' for row in mas for cell in row):
            win_label = tk.Label(screen, text="|o| выигрывает игрок №2 нолик",
                                 font=("Arial", 20), fg='black')
            win_label.place(x=780, y=550)
            step = ''
            step2 = ''
        elif all(cell != 'o' for row in mas for cell in row):
            win_label = tk.Label(screen, text="|x| выигрывает игрок №1 крестик",
                                 font=("Arial", 20), fg='black')
            win_label.place(x=780, y=550)
            step = ''
            step2 = ''
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
    screen.protocol("WM_DELETE_WINDOW", lambda: close_game(screen, menu))

def show_rules():
    rules_window = tk.Toplevel()
    rules_window.title("Правила игры")
    rules_window.geometry("1450x850+120+50")

    rules_window.image = tk.PhotoImage(file='Fon1_out.png')
    bg_logo = tk.Label(rules_window, image=rules_window.image)
    bg_logo.place(x=0, y=0, relwidth=1, relheight=1)
    rules_window.resizable(False, False)

    def back_to_menu2():
        rules_window.destroy()

    rules_text = """
    Правила игры:
    Данная игра рассчитана на двух игроков, которая проходит на игровом поле размером 
    10 на 10 клеток. Обозначениями становятся «крестик» и «нолик», обозначающие символы 
    каждого из игроков. 
    Начало игры происходит из противоположных углов игрового поля: крестик - левая верхняя клетка, 
    нолик - правая нижняя. 
    За один ход каждый из игроков может выполнить на выбор любую комбинацию из 3 действий:   
    - РАЗМНОЖЕНИЕ – игрок ставит один свой символ в незанятую клетку;    
    - ЗАРАЖЕНИЕ – заражение клетки с символом противника.
    Зараженные клетки "x" становятся красными и переходят в подчинение кружкам, а зараженные 
    "o" – синими и переходят в подчинение крестикам. 
    ЦЕЛЬ ИГРЫ: заразить все клетки с символом противника.
    Любые действия возможны только в ДОСТУПНЫХ для игрока клетках, то есть в тех, которые 
    расположены "по соседству" от клетки с символом игрока (x/o) или от зараженных в их подчинении.   
    Игра заканчивается, когда один игрок заражает все клетки с символом противника.
    Побеждает тот, кто заражает все клетки с символом противника.
    Во время игры можно ПРОПУСТИТЬ свой ХОД при отсутствии допустимого действия/хода по мнению игрока, 
    или добавить тем самым азарта игре, но тщательно обдумайте свое решение!
    """

    rules_label = tk.Label(rules_window, text=rules_text,bg='thistle3', font=("Helvetica", 16), justify="left")
    rules_label.pack(pady=25)

    return_button = tk.Button(rules_window, text="Назад", width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'), command=back_to_menu2)
    return_button.place(relx=0.5, rely=0.88, anchor="center")

def close_game(game_screen, menu):
    game_screen.destroy()
    menu.deiconify()  # Восстанавливаем окно меню
def open_menu():
    global start_the_game  # Скрываем главное окн0
    menu = tk.Tk()
    menu.title("Главное меню")
    menu.geometry("1450x850+120+50")
    menu.image = tk.PhotoImage(file='Fon2_out.png')
    bg_logo = tk.Label(menu, image=menu.image)
    bg_logo.place(x=0, y=0, relwidth=1, relheight=1)
    menu.resizable(False, False)
    play_button = tk.Button(menu, text='Играть', width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                      command=lambda: start_the_game(menu))
    play_button.place(relx=0.5, rely=0.45, anchor= "center")

    btn_rules = tk.Button(menu, text='Правила', width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                       command=show_rules)
    btn_rules.place(relx=0.5, rely=0.625, anchor="center")

    exit_button = tk.Button(menu, text='Выход', width=12, bg='plum4', fg='white', font=('Century', 25, 'bold'),
                        command=menu.destroy)
    exit_button.place(relx=0.5, rely=0.8, anchor= "center")
    menu.mainloop()

open_menu()
