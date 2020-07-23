# -*- coding: utf-8 -*-
import wx
import wx.xrc
import wx.grid
import sys
import sqlite3
import traceback

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


def main():
    app = Product()
    app.MainLoop()


class Product(wx.App):
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):   # noqa
        super().__init__(redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


###########################################################################
# Python code generated with wxFormBuilder (version Jun 17 2015)
# http://www.wxformbuilder.org/
###########################################################################
class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=u"Product wxPython grid", pos=wx.DefaultPosition,
                          size=wx.Size(500, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # Запрос на создание таблицы в БД
        query = 'CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)' \
            .format(TABLE_NAME)
        run_query(query)

        query = 'PRAGMA table_info({})'.format(TABLE_NAME)
        db_rows = run_query(query)

        self.db_field = []
        self.db_field_type = []
        for row in db_rows:
            self.db_field.append(row[1])  # Имена полей в БД и таблице `grid_data`
            self.db_field_type.append(row[2])  # Типы данных полей в БД

        # Имена полей в таблице `grid_data`
        self.grid_field = ['№', 'Наименование', 'Цена']
        # Переменные для сортировки элементов в таблице `grid_data`
        self.sort_name = ''
        self.sort_order = ''
        # Переменные для фильтрации элементов в таблице `grid_data`
        self.filter_name_tmp = ''
        self.filter_data_tmp = ''
        self.filter_name = ''
        self.filter_data = ''

        # Формируем панель-подложку на фрейме для переходов между виджетами по клавише TAB
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        vszr_frame = wx.BoxSizer(wx.VERTICAL)
        self.pnl_frame = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        # Глобальный распределитель виджетов по вертикали
        vszr_global = wx.BoxSizer(wx.VERTICAL)

        # Формируем надпись и поле ввода `name`
        self.pnl_name = wx.Panel(self.pnl_frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.pnl_name.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.pnl_name.SetFont(wx.Font(12, 70, 90, 90, False, "Courier"))
        self.pnl_name.SetMaxSize(wx.Size(-1, 35))

        hszr_name = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_name = wx.StaticText(self.pnl_name, wx.ID_ANY, u"Name :", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lbl_name.Wrap(-1)
        hszr_name.Add(self.lbl_name, 0, wx.ALL, 5)

        self.entry_name = wx.TextCtrl(self.pnl_name, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        hszr_name.Add(self.entry_name, 1, wx.ALL, 5)

        self.pnl_name.SetSizer(hszr_name)
        self.pnl_name.Layout()
        hszr_name.Fit(self.pnl_name)
        vszr_global.Add(self.pnl_name, 0, wx.ALL | wx.EXPAND, 5)

        # Формируем надпись и поле ввода `price`
        self.pnl_price = wx.Panel(self.pnl_frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.pnl_price.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.pnl_price.SetFont(wx.Font(12, 70, 90, 90, False, "Courier"))
        self.pnl_price.SetMaxSize(wx.Size(-1, 35))

        hszr_price = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_price = wx.StaticText(self.pnl_price, wx.ID_ANY, u"Price :", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lbl_price.Wrap(-1)
        hszr_price.Add(self.lbl_price, 0, wx.ALL, 5)

        self.entry_price = wx.TextCtrl(self.pnl_price, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        hszr_price.Add(self.entry_price, 1, wx.ALL, 5)

        self.pnl_price.SetSizer(hszr_price)
        self.pnl_price.Layout()
        hszr_price.Fit(self.pnl_price)
        vszr_global.Add(self.pnl_price, 0, wx.ALL | wx.EXPAND, 5)

        # Формируем текст сообщений на форме
        self.message = wx.StaticText(self.pnl_frame, wx.ID_ANY, '', wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.message.Wrap(-1)
        self.message.SetFont(wx.Font(11, 70, 90, 90, False, "Tahoma"))
        self.message.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.message.SetMaxSize(wx.Size(-1, 35))
        vszr_global.Add(self.message, 0, wx.ALL | wx.EXPAND, 5)

        # Формируем таблицу `grid_data`
        self.grid_data = wx.grid.Grid(self.pnl_frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.DOUBLE_BORDER)

        #   Grid
        self.grid_data.CreateGrid(0, len(self.grid_field), wx.grid.Grid.SelectRows)
        self.grid_data.EnableEditing(False)
        self.grid_data.EnableGridLines(True)
        self.grid_data.EnableDragGridSize(False)
        self.grid_data.SetMargins(0, 0)

        #   Columns
        self.grid_data.SetDefaultColSize(80, resizeExistingCols=True)
        self.grid_data.SetColMinimalAcceptableWidth(80)
        # self.grid_data.SetColSize(0, 60)
        self.grid_data.SetColSize(1, 240)
        # self.grid_data.SetColSize(2, 100)
        # self.grid_data.AutoSizeColumns()
        self.grid_data.EnableDragColMove(False)
        self.grid_data.EnableDragColSize(True)
        self.grid_data.SetColLabelSize(30)
        for i in range(len(self.grid_field)):
            self.grid_data.SetColLabelValue(i, self.grid_field[i])
            # Определяем столбец как float с выравниванием значений по умолчанию(справа) и 2 знаками после ','
            if self.grid_field[i] == 'Цена':
                self.grid_data.SetColFormatFloat(i, width=-1, precision=2)
        self.grid_data.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        #   Rows
        self.grid_data.AutoSizeRows()
        self.grid_data.EnableDragRowSize(False)
        self.grid_data.SetRowLabelSize(40)
        self.grid_data.SetRowLabelAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)

        #   Label Appearance
        self.grid_data.UseNativeColHeader(False)  # True - для отображения сортировки в заголовке столбца
        self.grid_data.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.grid_data.SetLabelFont(wx.Font(12, 70, 90, 90, False, "Tahoma"))
        self.grid_data.SetLabelTextColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        #   Cell Defaults
        self.grid_data.SetDefaultCellFitMode(wx.grid.GridFitMode.Ellipsize())
        self.grid_data.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.grid_data.SetDefaultCellFont(wx.Font(11, 70, 90, 90, False, "Arial"))

        # Формируем контекстное меню на `grid_data`
        self.pop_menu = wx.Menu()
        self.pm_setfil = wx.MenuItem(self.pop_menu, wx.ID_ANY, u"Set filter", wx.EmptyString, wx.ITEM_NORMAL)
        self.pm_clrfil = wx.MenuItem(self.pop_menu, wx.ID_ANY, u"Clear filter", wx.EmptyString, wx.ITEM_NORMAL)
        self.pop_menu.Append(self.pm_setfil)
        self.pop_menu.Append(self.pm_clrfil)
        self.grid_data.Bind(wx.EVT_CONTEXT_MENU, self.grid_dataOnGridCellRightClick)
        vszr_global.Add(self.grid_data, 1, wx.ALL | wx.EXPAND, 5)

        # Формируем кнопок `Add`, `Edit`, `Del`
        self.pnl_btn = wx.Panel(self.pnl_frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.pnl_btn.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.pnl_btn.SetFont(wx.Font(12, 70, 90, 90, False, "Courier"))

        hszr_but = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_add = wx.Button(self.pnl_btn, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize,
                                 0 | wx.DOUBLE_BORDER)
        self.btn_add.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        hszr_but.Add(self.btn_add, 1, wx.ALL, 5)

        self.btn_edit = wx.Button(self.pnl_btn, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.DefaultSize,
                                  0 | wx.DOUBLE_BORDER)
        self.btn_edit.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        hszr_but.Add(self.btn_edit, 1, wx.ALL, 5)

        self.btn_del = wx.Button(self.pnl_btn, wx.ID_ANY, u"Del", wx.DefaultPosition, wx.DefaultSize,
                                 0 | wx.DOUBLE_BORDER)
        self.btn_del.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        hszr_but.Add(self.btn_del, 1, wx.ALL, 5)

        self.pnl_btn.SetSizer(hszr_but)
        self.pnl_btn.Layout()
        hszr_but.Fit(self.pnl_btn)
        vszr_global.Add(self.pnl_btn, 0, wx.ALL | wx.EXPAND, 5)
        #

        self.pnl_frame.SetSizer(vszr_global)
        self.pnl_frame.Layout()
        vszr_global.Fit(self.pnl_frame)
        vszr_frame.Add(self.pnl_frame, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vszr_frame)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_SIZE, self.form_resize)
        self.entry_name.Bind(wx.EVT_CHAR, self.OnKeyPress)
        self.entry_price.Bind(wx.EVT_CHAR, self.OnKeyPress)
        self.grid_data.Bind(wx.EVT_CHAR, self.OnKeyPress)
        self.grid_data.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        self.grid_data.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.grid_dataOnGridCellLeftClick)
        self.grid_data.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.grid_dataOnGridCellRightClick)
        self.grid_data.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.grid_dataOnGridLabelLeftClick)
        self.grid_data.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.grid_dataOnGridRangeSelect)

        self.Bind(wx.EVT_MENU, self.pm_setfilOnMenuSelect, id=self.pm_setfil.GetId())
        self.Bind(wx.EVT_MENU, self.pm_clrfilOnMenuSelect, id=self.pm_clrfil.GetId())

        self.btn_add.Bind(wx.EVT_BUTTON, self.add_click)
        self.btn_edit.Bind(wx.EVT_BUTTON, self.edit_click)
        self.btn_del.Bind(wx.EVT_BUTTON, self.del_click)

        # Отображение таблицы
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)

    def view_rec(self, sort_name='', sort_order='', filter_name='', filter_data=''):
        """Отображение данных в таблице `grid_data`"""
        # Очистка `grid_data`
        if self.grid_data.GetNumberRows() > 0:
            self.grid_data.DeleteRows(0, self.grid_data.GetNumberRows())
        # Запросы к БД с фильтрацией и сортировкой записей
        if filter_name != '':
            params = (filter_data,)
            if sort_name != '':
                query = 'SELECT * FROM {} WHERE {} = ? ORDER BY {} {}'.format(TABLE_NAME, filter_name,
                                                                              sort_name, sort_order)
            else:
                query = 'SELECT * FROM {} WHERE {} = ?'.format(TABLE_NAME, filter_name)
            self.message.Label = 'Table {} filtered'.format(TABLE_NAME)
        else:
            params = ()
            query = 'SELECT * FROM {} ORDER BY {} {}'.format(TABLE_NAME, sort_name, sort_order) \
                if sort_name != '' \
                else 'SELECT * FROM {}'.format(TABLE_NAME)
            self.message.Label = 'Full table {} is displayed'.format(TABLE_NAME)

        # Выборка данных из базы
        db_rows = run_query(query, params)
        # Заполнение таблицы
        if db_rows is not None:
            sum_col = [None for _ in range(self.grid_data.NumberCols)]
            r = 0
            for row in db_rows:
                self.grid_data.AppendRows(1)
                for c in range(self.grid_data.NumberCols):
                    self.grid_data.SetCellValue(r, c, str(row[c]))
                    # Выравниваем значения в ячейках по центру
                    if self.grid_data.GetColLabelValue(c) == '№':
                        self.grid_data.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_TOP)
                    # подсчет данных для итогов
                    if self.db_field_type[c] == 'INTEGER' or self.db_field_type[c] == 'REAL':
                        try:
                            if sum_col[c] is None:
                                sum_col[c] = float(row[c])  # noqa
                            else:
                                sum_col[c] += float(row[c])
                        except ValueError:
                            pass  # print('ValueError', c)
                r += 1
            # Итоги
            self.total_line(r, sum_col)
        else:
            self.message.label = 'Query error DB: {}, table: {}.'.format(DB_NAME, TABLE_NAME)

    def total_line(self, r=0, sum_col=None):
        """Добавляет в конец таблицы итоги исходя из переданных данных.

        Args:
            r (int): количество строк в таблице.
            sum_col (list): список с итоговыми данными по столбцам.
        """
        if r > 0:
            self.grid_data.AppendRows(1)
            attr = wx.grid.GridCellAttr()
            attr.SetBackgroundColour('pink')
            self.grid_data.SetRowAttr(r, attr)
            self.grid_data.SetCellValue(r, 1, 'Среднее значение:')
            try:
                self.grid_data.SetCellValue(r, 2, str(round(float(sum_col[2]) / r, 2)))
            except TypeError:
                self.grid_data.SetCellValue(r, 2, '-')

    def clear_entry(self):
        """Очищает поля ввода/редактирования."""
        self.entry_name.Clear()
        self.entry_price.Clear()

    def select_row_get(self):
        """Определяет список выделенных записей в таблице `grid_data`.

        return [(row_values), ...]
            Возвращает список с кортежами данных выделенных строк в таблице `grid_data`.
        """
        # Очистка списка и полей формы
        sel_list = []
        self.clear_entry()
        # Формирование списка выделенных строк
        for row in self.grid_data.GetSelectedRows():
            sel_row = []
            color = self.grid_data.GetCellBackgroundColour(row, 0)
            if color[1] == 255:  # добавляем только белые строки
                for col in range(self.grid_data.NumberCols):
                    sel_row.append(self.grid_data.GetCellValue(row, col))
                sel_list.append(tuple(sel_row))
        # Заполнение полей ввода значениями, если выделена одна запись
        if len(sel_list) == 1:
            try:
                self.entry_name.SetValue(sel_list[0][1])
                self.entry_price.SetValue(sel_list[0][2])
            except IndexError:
                self.message.Label = 'No selected row(IndexError:select_row_get)'
                return []
        # Формирование списка выделенных `id`, только для вывода в `self.message`!!!
        ids = []
        for i in sel_list:
            ids.append(i[0])
        self.message.Label = 'Selected row id={}'.format(ids)
        # Возврат результата
        return sel_list

    # Virtual event handlers, overide them in your derived class
    def form_resize(self, event):
        """Отслеживает изменение размеров формы и корректирует виджеты."""
        sz = wx.Window.GetSize(self)
        # Изменяем ширину столбца `name` в зависимости от размера фрейма
        if sz[0] >= 500:
            self.grid_data.SetColSize(1, sz[0]-260)
        else:
            self.grid_data.SetColSize(1, 240)
        event.Skip()

    def grid_dataOnGridCellLeftClick(self, event):  # noqa
        """Очищает поля ввода/редактирования при снятии выделения."""
        if not event.Selecting():
            self.message.Label = 'No selected row'
            self.clear_entry()
        event.Skip()

    def grid_dataOnGridCellRightClick(self, event): # noqa
        """Определяет временные переменные поля `filter_name_tmp` и значения `filter_data_tmp` для фильтрации,
        а так же, определяет содержимое контекстного меню.
        """
        try:
            self.filter_name_tmp = self.db_field[event.GetCol()] if event.GetCol() >= 0 else ''
            self.filter_data_tmp = self.grid_data.GetCellValue(event.GetRow(), event.GetCol())
            self.grid_data.GoToCell(event.GetRow(), event.GetCol())
            # Изменяем состав пунктов контекстного меню
            if self.pop_menu.GetMenuItemCount() == 1:
                self.pop_menu.Remove(self.pm_clrfil)
                self.pop_menu.Append(self.pm_setfil)
                self.pop_menu.Append(self.pm_clrfil)
        except AttributeError:
            self.filter_name_tmp = ''
            self.filter_data_tmp = ''
            # Изменяем состав пунктов контекстного меню
            if self.pop_menu.GetMenuItemCount() > 1:
                self.pop_menu.Remove(self.pm_setfil)

        self.grid_data.PopupMenu(self.pop_menu)
        event.Skip()

    def grid_dataOnGridLabelLeftClick(self, event): # noqa
        """Определяет переменные поля `sort_name` и порядка `sort_order` сортировки данных в таблице `grid_data`."""
        if event.GetCol() >= 0:
            if self.grid_data.IsSortingBy(event.GetCol()) and self.grid_data.IsSortOrderAscending():
                self.sort_order = 'DESC'
                self.grid_data.SetSortingColumn(event.GetCol(), False)
                self.grid_data.SetColLabelValue(event.GetCol(), self.grid_field[event.GetCol()] + '  v')
            else:
                self.sort_order = ''
                self.grid_data.SetSortingColumn(event.GetCol(), True)
                if self.sort_name != '':
                    self.grid_data.SetColLabelValue(self.db_field.index(self.sort_name),
                                                    self.grid_field[self.db_field.index(self.sort_name)])
                self.grid_data.SetColLabelValue(event.GetCol(), self.grid_field[event.GetCol()] + '  ^')
            self.sort_name = self.db_field[event.GetCol()]
            self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
        event.Skip()

    def grid_dataOnGridRangeSelect(self, event):    # noqa
        """Формирование списка выделенных строк."""
        if event.Selecting():
            self.select_row_get()
        event.Skip()

    def OnKeyPress(self, event):    # noqa
        """Определяет поведение виджетов при нажатии клавиш клавиатуры."""
        if event.GetKeyCode() == wx.WXK_TAB:  # Tab
            self.grid_data.Navigate()
        elif event.GetKeyCode() == 1:  # Ctrl+a
            self.add_click(event)
        elif event.GetKeyCode() == 5:  # Ctrl+e
            self.edit_click(event)
        elif event.GetKeyCode() == 4:  # Ctrl+d
            self.del_click(event)
        event.Skip()

    def pm_setfilOnMenuSelect(self, event): # noqa
        """Определяет переменные поля `filter_name` и значения `filter_data` для фильтрации записей,
        отображаемых в таблице `grid_data`.
        """
        self.filter_name = self.filter_name_tmp
        self.filter_data = self.filter_data_tmp
        self.message.Label = 'No selected row'
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
        event.Skip()

    def pm_clrfilOnMenuSelect(self, event): # noqa
        """Очищает переменные фильтра для записей отображаемых в таблице `grid_data`."""
        self.filter_name = ''
        self.filter_data = ''
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
        event.Skip()

    def add_click(self, event):
        """Добавление данных в таблицу БД."""
        try:
            price = float(self.entry_price.GetValue().replace(',', '.'))
        except ValueError:
            self.message.Label = 'Entry not correct!(ValueError:record_add)'
            return

        name = self.entry_name.GetValue().strip()

        if len(name) > 0 and price >= 0:
            query = 'INSERT INTO {} VALUES(NULL,?,?)'.format(TABLE_NAME)
            params = (name, price)
            run_query(query, params)
            self.clear_entry()
            self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
            self.message.Label = 'Record added'
        else:
            self.message.Label = 'Entry not correct!'
        event.Skip()

    def edit_click(self, event):
        """Изменение данных в таблице БД."""
        try:
            price = float(self.entry_price.GetValue().replace(',', '.'))
        except ValueError:
            self.message.Label = 'Entry not correct!(ValueError:record_edit)'
            return

        name = self.entry_name.GetValue().strip()
        sel_list = self.select_row_get()

        if len(name) > 0 and price >= 0:
            query = 'UPDATE {} SET name=?, price=? WHERE id=?'.format(TABLE_NAME)
            for i in sel_list:
                params = (name, price, i[0])
                run_query(query, params)
            self.clear_entry()
            self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
            self.message.Label = 'Record edited'
        else:
            self.message.Label = 'Entry not correct!'
        event.Skip()

    def del_click(self, event):
        """Удаление данных из таблицы БД."""
        query = 'DELETE FROM {} WHERE id=?'.format(TABLE_NAME)

        sel_list = self.select_row_get()

        for i in sel_list:
            try:
                params = (i[0],)
            except IndexError:
                self.message.Label = 'No selected row(IndexError:record_delete)'
                return
            else:
                run_query(query, params)

        self.clear_entry()
        self.view_rec(self.sort_name, self.sort_order, self.filter_name, self.filter_data)
        self.message.Label = 'Row deleted'
        event.Skip()


if __name__ == '__main__':
    main()
