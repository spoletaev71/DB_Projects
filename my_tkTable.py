# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import ttk
import sqlite3
import traceback

# Задачи на разработку:
# 1. Обработка множественного выбора строк с клавиатуры в таблице.

DB_NAME = 'DataBase.db'     # Наименование БД типа `sqlite3` (если не существует, то создаётся новая)
TABLE_NAME = 'product'      # Наименование таблицы в БД (если не существует, то создаётся новая)


def run_query(query, params=()):
    """Подллючение к БД и выполнение запроса."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, params)
            conn.commit()
        return query_result
    except Exception:  # noqa # Отлавливаем широкий круг ошибок для вывода в консоль
        print("Exception in user code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)
        return 'None'


class MyTree(ttk.Treeview):
    """Класс-наследник `ttk.Treeview` с возможностью подсвечивания строк цветом
    фона при вставке(метод `insert`), в зависимости от содержимого выводимых данных.
    Подсмотрел тут:    https://ru.stackoverflow.com/questions/1074824
    """
    def __init__(self, *args, **kwargs):
        """Элементам с тегом even(четные) назначить цвет фона aquamarine,
         а элементам с тегом odd(нечетные) назначить цвет фона lightyellow.
        """
        super().__init__(*args, **kwargs)
        self.tag_configure('total', background='pink')
        self.tag_configure('even', background='aquamarine')
        self.tag_configure('odd', background='lightyellow')

    def insert(self, parent_node, index, **kwargs):
        """Назначение тега при добавлении элемента в таблицу"""
        item = super().insert(parent_node, index, **kwargs)
        values = kwargs.get('values', None)
        if values:
            if type(values[0]) != int:
                super().item(item, tag='total')
            elif values[0] % 2 == 0:
                super().item(item, tag='even')
            else:
                super().item(item, tag='odd')
        return item


class Product:
    def __init__(self, window):

        def fixed_map(option):
            return [elm for elm in self.style.map('Treeview', query_opt=option) if
                    elm[:-1] != ('!disabled', '!selected')]

        self.window = window
        self.window.geometry('500x500+800+10')
        self.window.title('Product tkinter grid')
        # self.window.resizable(False, False)   # Запрет изменения размеров окна
        self.window.protocol("WM_DELETE_WINDOW", lambda: sys.exit())

        self.arrow_up = tk.PhotoImage(file='purple-arrow-up-1.gif')
        self.arrow_down = tk.PhotoImage(file='purple-arrow-down-1.gif')

        # Запрос на создание таблицы в БД
        query = 'CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)'\
            .format(TABLE_NAME)
        run_query(query)

        query = 'PRAGMA table_info({})'.format(TABLE_NAME)
        db_rows = run_query(query)

        self.db_field = []
        self.db_field_type = []
        for row in db_rows:
            self.db_field.append(row[1])        # Имена полей в БД и таблице `grid_data`
            self.db_field_type.append(row[2])   # Типы данных полей в БД

        # Соответствие имен полей в БД и в таблице `Treeview`
        field_name = {'id': '№', 'name': 'Наименование', 'price': 'Цена'}

        # Переменные для сортировки элементов в таблице `Treeview`
        self.sort_name = ''
        self.sort_order = ''
        # Переменные для фильтрации элементов в таблице `Treeview`
        self.filter_name = ''
        self.filter_data = ''
        self.x = 0

        # Фрейм с элементами редактирования наименованя
        fr_name = tk.Frame()
        fr_name.pack(side=tk.TOP, fill=tk.X)
        tk.Label(fr_name, justify=tk.LEFT, text=' Name:', font='courier 12').pack(side=tk.LEFT, padx=20, pady=10)
        self.entry_name = tk.Entry(fr_name, justify=tk.RIGHT, font='arial 11')
        self.entry_name.pack(side=tk.RIGHT, padx=10, expand=1, fill=tk.X)

        # Фрейм с элементами редактирования цены
        fr_price = tk.Frame()
        fr_price.pack(side=tk.TOP, fill=tk.X)
        tk.Label(fr_price, justify=tk.LEFT, text=' Price:', font='courier 12').pack(side=tk.LEFT, padx=20, pady=10)
        self.entry_price = tk.Entry(fr_price, justify=tk.RIGHT, font='arial 11')
        self.entry_price.pack(side=tk.RIGHT, padx=10, expand=1, fill=tk.X)

        # Сообщения на форме (!!!для контроля!!!)
        self.message = tk.Label(text='', bg='lightblue', font='tahoma 11')
        self.message.pack(padx=10, pady=10, fill=tk.X)

        # Стилистика отображеня таблицы `Treeview`
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        self.style.configure("Treeview", font='arial 11')
        self.style.configure('Treeview.Heading', font='tahoma 12', foreground='blue')

        # Таблица `Treeview`
        self.tree = MyTree(columns=self.db_field, displaycolumns=([i for i in range(len(self.db_field))]),
                           show='headings', padding=(0, 0, 16, 0), selectmode='extended', takefocus=True)
        # Полоса прокрутки таблицы `Treeview`
        yscroll = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscrollcommand=yscroll.set)
        # Столбцы таблицы фиксированного размера `Treeview`
        self.tree.column(self.db_field[0], width=60, stretch=False, anchor=tk.CENTER)
        self.tree.column(self.db_field[1], width=200, anchor=tk.W)
        self.tree.column(self.db_field[2], width=140, stretch=False, anchor=tk.E)
        # Шапка таблицы `Treeview`
        for f in self.db_field:
            self.tree.heading(f, text=field_name.get(f), anchor=tk.CENTER)
        # Полное контекстное меню для заполненной части таблицы `Treeview`
        self.popup_menu_filter_full = tk.Menu(self.tree, tearoff=0)
        self.popup_menu_filter_full.add_command(label="Set filter", command=self.filter_set)
        self.popup_menu_filter_full.add_command(label="Clear filter", command=self.filter_remove)
        # Урезаное контекстное меню для пустой части таблицы `Treeview`
        self.popup_menu_filter_clear = tk.Menu(self.tree, tearoff=0)
        self.popup_menu_filter_clear.add_command(label="Clear filter", command=self.filter_remove)
        # Обработка действий мыши и клавиш в таблице
        self.tree.bind('<ButtonRelease-1>', self.click_tree)
        self.tree.bind("<Button-3>", self.click_tree)
        self.tree.bind('<space>', self.select_one)
        self.tree.bind('<Control-space>', self.select_multiple)     # TODO
        #
        self.tree.pack(padx=10, expand=1, fill=tk.BOTH)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Фрейм с кнопками редактирования
        fr_but = tk.Frame()
        fr_but.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        bt_add = tk.Button(fr_but, text='Add', width=8, font='courier 12', command=self.record_add)
        bt_edt = tk.Button(fr_but, text='Edit', width=8, font='courier 12', command=self.record_edit)
        bt_del = tk.Button(fr_but, text='Del', width=8, font='courier 12', command=self.record_delete)
        bt_add.bind('<Return>', self.record_add)
        bt_edt.bind('<Return>', self.record_edit)
        bt_del.bind('<Return>', self.record_delete)
        bt_add.pack(side=tk.LEFT, padx=20)
        bt_edt.pack(side=tk.LEFT, expand=1, padx=20)
        bt_del.pack(side=tk.RIGHT, padx=20)

        # Отображение таблицы
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)

    def view_rec(self, sort_name='', sort_order='', filter_name='', filter_data=''):
        """Отображение данных в таблице `Treeview`"""
        # Очистка `treeview`
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Запросы к БД с фильтрацией и сортировкой записей таблицы `Treeview`
        if filter_name != '':
            params = (filter_data,)
            if sort_name != '':
                query = 'SELECT * FROM {} WHERE {} = ? ORDER BY {} {}'.format(TABLE_NAME, filter_name,
                                                                              sort_name, sort_order)
            else:
                query = 'SELECT * FROM {} WHERE {} = ?'.format(TABLE_NAME, filter_name)
            self.message['text'] = 'Table {} filtered by {}'.format(TABLE_NAME, filter_name)
        else:
            params = ()
            query = 'SELECT * FROM {} ORDER BY {} {}'.format(TABLE_NAME, sort_name, sort_order) \
                if sort_name != '' \
                else 'SELECT * FROM {}'.format(TABLE_NAME)
            self.message['text'] = 'Full table {} is displayed'.format(TABLE_NAME)

        # Выборка данных из базы
        db_rows = run_query(query, params)
        # Заполнение таблицы
        if db_rows != 'None':
            for row in db_rows:
                self.tree.insert('', tk.END, values=row)
            records = self.tree.get_children()
            if len(records) > 0:
                self.tree.focus(records[0])
                # Итоги
                self.total_line('sum', 2, 1, 'Итого:')
                self.total_line('qty.', 0)
        else:
            self.message['text'] = 'Query error DB: {}, table: {}.'.format(DB_NAME, TABLE_NAME)

    def total_line(self, func_total, column_total, column_comment=None, text_comment=None):
        """Добавляет в конец таблицы итоги по указанному столбцу.
         Повторный запуск с другой функцией и по другому столбцу дополнит итоговую строку.

        Args:
            func_total (str): определяет тип итогов для вывода и может принимать следующие
                значения: "qty.", "avg", "sum". Обязательный параметр. Если задан неверно,
                то итоги не выводятся.
            column_total (int): индекс поля по которому идет подсчет итогов. Обязательный параметр.
            column_comment (int): индекс поля для вывода надписи комментария. Если параметр не задан,
                то комментарий не выводится.
            text_comment (str): текст комментария к итоговой строке. Если параметр не задан,
                то комментарий не выводится.
        """
        # Если уже есть итоги, то запоминаем и удаляем из таблицы
        if self.tree.tag_has('total'):
            values_total = list(self.tree.item(self.tree.tag_has('total'), 'values'))
            self.tree.delete(self.tree.tag_has('total'))
            items = self.tree.get_children()
        else:                                               # Иначе формируем новые
            items = self.tree.get_children()
            values_total = ['' for _ in items[0]]
        # Запоминаем комментарий, если есть
        if column_comment is not None and text_comment is not None:
            values_total[column_comment] = text_comment
        # Определяемся с функцией итогов, расчитываем и запоминаем их
        if func_total == 'qty.':
            values_total[column_total] = str(len(items))    # Преобразуем в строку для задания нужного тэга
        elif func_total == 'avg' or func_total == 'sum':
            summa = 0
            for item in items:
                summa += float(self.tree.item(item, 'values')[column_total])
            if func_total == 'avg':     # average
                values_total[column_total] = str(round(summa / len(items), 2)) if len(items) > 0 else '-'
            elif func_total == 'sum':
                values_total[column_total] = str(summa)
        else:
            return
        # Выводим итоги в таблицу
        self.tree.insert('', tk.END, values=tuple(values_total))

    def clear_entry(self):
        """Очищает поля ввода/редактирования."""
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

    def filter_set(self):
        """Определяет фильтр для записей отображаемых в таблице `Treeview`"""
        sel_list = self.select_row_get()
        try:
            column_number = int(self.tree.identify_column(self.x).replace('#', '')) - 1
            self.filter_name = self.tree.column(self.tree.identify_column(self.x))['id']
            self.filter_data = sel_list[0][column_number]
        except IndexError:
            self.message['text'] = 'No selected row(IndexError:filter_set)'
            return
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)

    def filter_remove(self):
        """Очищает фильтр для записей отображаемых в таблице `Treeview`"""
        self.filter_name = ''
        self.filter_data = ''
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)

    def do_full_popup_menu(self, event_x, event_y):
        """Отображение полного контекстного меню."""
        try:
            self.popup_menu_filter_full.post(event_x, event_y)
        finally:
            self.popup_menu_filter_full.grab_release()

    def do_short_popup_menu(self, event_x, event_y):
        """Отображение урезаного контекстного меню."""
        try:
            self.popup_menu_filter_clear.post(event_x, event_y)
        finally:
            self.popup_menu_filter_clear.grab_release()

    def select_one(self, event):
        """Выбор записи находящейся в фокусе."""
        self.tree = event.widget
        self.tree.selection_set(self.tree.focus())
        self.select_row_get()

    def select_multiple(self, event):   # TODO
        """Выбор нескольких записей. !!! НЕДОПИЛЕНО !!!"""
        self.tree = event.widget
        sel_list = list(self.tree.selection())
        sel_list.append(self.tree.focus())
        self.tree.selection_set(tuple(sel_list))
        self.select_row_get()

    def click_tree(self, event):    # noqa
        """Определяет выбираемое действие в таблице `Treeview`: выделение записей, сортировка или вызов меню фильтрации.

        1. Если нажатие в области данных (`cell`), то выполнение передается функции `select_row_get()`
        для определения выделения либо отрисовка полного контекстного меню фильтрации (`popup_menu_filter_full`)
        для установки либо отмены фильтра.

        2. Если нажатие в пустой области (`tree`), то выполнение передается функции `select_row_get()`
        для определения выделения либо отрисовка урезанного контекстного меню фильтрациии (`popup_menu_filter_clear`)
        для возможности отключения фильтра.

        3. Если нажатие в области заголовка (`heading`), то выполнение передается функции select_head()
        для определения поля сортировки по координате `event.x`.

        4. Если нажатие в пустой области (`nothing` или `tree`), то только отрисовка урезанного контекстного
        меню фильтрациии (`popup_menu_filter_clear`) для возможности отключения фильтра.
        """
        region = self.tree.identify_region(event.x, event.y)
        if region == 'cell':  # Область данных
            if event.num == 3:  # Только для правой кнопки мыши:
                self.tree.selection_set(self.tree.identify_row(event.y))  # выделение строки
                self.x = event.x  # сохранение `x` для определения столбца
                self.do_full_popup_menu(event.x_root, event.y_root)
            self.select_row_get()
        elif region == 'tree':  # Область справа от данных
            if event.num == 1:  # Только для левой кнопки мыши
                self.select_row_get()
            elif event.num == 3:
                self.do_short_popup_menu(event.x_root, event.y_root)
        elif region == 'heading':  # Область заголовков
            if event.num == 1:
                self.select_head(event.x)
        elif region == 'nothing':  # Пустая область ниже данных
            if event.num == 3:
                self.do_short_popup_menu(event.x_root, event.y_root)
        else:
            self.message['text'] = 'No select row'

    def select_row_get(self):
        """Определяет список выделенных записей в таблице `Treeview`.

        return [(row_values), ...]
            Возвращает список с кортежами данных выделенных строк в таблице `Treeview`.
        """
        # Очистка списка и полей формы
        sel_list = []
        self.clear_entry()
        # Формирование списка выделенных строк
        for i in self.tree.selection():
            if not self.tree.tag_has('total', i):
                sel_list.append(self.tree.item(i, 'values'))
        # Заполнение полей ввода значениями, если выделена одна запись
        if len(sel_list) == 1:
            try:
                self.entry_name.insert(0, sel_list[0][1])
                self.entry_price.insert(0, sel_list[0][2])
            except IndexError:
                self.message['text'] = 'No selected row(IndexError:select_row_get)'
                return []
        # Формирование списка выделенных `id`, только для вывода в `self.message`!!!
        ids = []
        for i in sel_list:
            ids.append(i[0])
        self.message['text'] = 'Selected row id={}'.format(ids)
        # Возврат результата
        return sel_list

    def select_head(self, event_x):
        """Определяет переменные поля `sort_name` и порядока `sort_order` сортировки данных в таблице `Treeview`."""
        column_name = self.tree.column(self.tree.identify_column(event_x))['id']

        if self.sort_name == column_name and self.sort_order == '':
            if self.sort_order == '':
                self.sort_order = 'DESC'
                self.tree.heading(column_name, image=self.arrow_down)
        else:
            self.sort_order = ''
            if self.sort_name != '':
                self.tree.heading(self.sort_name, image='')
            self.tree.heading(column_name, image=self.arrow_up)

        self.sort_name = column_name
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)

    def record_add(self, event=None):   # noqa
        """Добавление данных в таблицу БД"""
        try:
            price = float(self.entry_price.get().replace(',', '.'))
        except ValueError:
            self.message['text'] = 'Entry not correct!(ValueError:record_add)'
            return

        name = self.entry_name.get().strip()

        if len(name) > 0 and price >= 0:
            query = 'INSERT INTO {} VALUES(NULL,?,?)'.format(TABLE_NAME)
            params = (name, price)
            run_query(query, params)
            self.clear_entry()
            self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
            self.message['text'] = 'Record added'
        else:
            self.message['text'] = 'Entry not correct!'

    def record_edit(self, event=None):  # noqa
        """Изменение данных в таблице БД"""
        try:
            price = float(self.entry_price.get().replace(',', '.'))
        except ValueError:
            self.message['text'] = 'Entry not correct!(ValueError:record_edit)'
            return

        name = self.entry_name.get().strip()
        sel_list = self.select_row_get()

        if len(name) > 0 and price >= 0:
            query = 'UPDATE {} SET name=?, price=? WHERE id=?'.format(TABLE_NAME)
            for i in sel_list:
                params = (name, price, i[0])
                run_query(query, params)
            self.clear_entry()
            self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
            self.message['text'] = 'Record edited'
        else:
            self.message['text'] = 'Entry not correct!'

    def record_delete(self, event=None):    # noqa
        """Удаление данных из таблицы БД"""
        query = 'DELETE FROM {} WHERE id=?'.format(TABLE_NAME)

        sel_list = self.select_row_get()

        for i in sel_list:
            try:
                params = (i[0],)
            except IndexError:
                self.message['text'] = 'No selected row(IndexError:record_delete)'
                return
            else:
                run_query(query, params)

        self.clear_entry()
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
        self.message['text'] = 'Row deleted'


if __name__ == '__main__':
    root = tk.Tk()
#    print(root.tk.call('info', 'patchlevel'))    # tkinter version
    app = Product(root)
    root.mainloop()
