import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QTableWidgetItem


class MyWindow(QMainWindow):
    all_result = []

    def __init__(self):
        super().__init__()
        uic.loadUi('F.ui', self)
        self.con = sqlite3.connect('films.db')
        self.cur = self.con.cursor()

        sup_list = self.cur.execute('SELECT * FROM genres').fetchall()
        sup_list = [i[1] for i in sup_list]
        self.comboBox.addItems(sup_list)

        self.search_one.clicked.connect(self.find_all)
        self.search_two.clicked.connect(self.find_name)
        self.change.clicked.connect(self.edit_cell)
        self.push.clicked.connect(self.add_new_element)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Год', 'Длительность'])

        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    
    #вывести на экран окошко с добавлением
    def add_new_element(self):
        add.show()
        

    def find_name(self):
        name = self.name.text()
        self.all_result = self.cur.execute(f'SELECT * FROM Films WHERE title like \'%{name}%\'').fetchmany(150)
        self.fout()

    def find_all(self):
        data = self.data.text()
        time = self.time.text()
        genre = self.comboBox.currentText()

        if genre == 'Не выбрано':
            if data and time:
                result = f'SELECT * FROM Films WHERE year = \'{data}\' AND duration = \'{time}\''
            if data and not time:
                result = f'SELECT * FROM Films WHERE year = \'{data}\''
            if time and not data:
                result = f'SELECT * FROM Films WHERE duration = \'{time}\''
            if not time and not data:
                result = f'SELECT * FROM Films'
        else:
            support = self.cur.execute(f'SELECT * FROM genres WHERE title = \'{genre}\'').fetchall()
            result = f'SELECT * FROM Films WHERE genre = \'{support[0][0]}\''
            if time:
                result += f' AND duration = \'{time}\''
            if data:
                result += f' AND year = \'{data}\''

        self.all_result = self.cur.execute(result).fetchmany(150)
        self.fout()

    def fout(self):
        self.table.setRowCount(0)
        for index, elements in enumerate(self.all_result):
            self.table.setRowCount(self.table.rowCount() + 1)
            item = QTableWidgetItem(str(elements[0]))
            #указываю, что нельзя редактировать
            item.setFlags(Qt.ItemIsEditable)
            self.table.setItem(index, 0, item)
            self.table.setItem(index, 1, QTableWidgetItem(elements[1]))
            self.table.setItem(index, 2, QTableWidgetItem(str(elements[2])))
            self.table.setItem(index, 3, QTableWidgetItem(str(elements[4])))

        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def edit_cell(self):
        new_table = []
        old_table = []
        for i in range(len(self.all_result)):
            sup_id = str(self.all_result[i][0])
            sup_name = str(self.all_result[i][1])
            sup_year = str(self.all_result[i][2])
            sup_time = str(self.all_result[i][3])
            old_table.append((sup_id, sup_name, sup_year, sup_time))
            sup_id = self.table.item(i, 0).text()
            sup_name = self.table.item(i, 1).text()
            sup_year = self.table.item(i, 2).text()
            sup_time = self.table.item(i, 3).text()
            new_table.append((sup_id, sup_name, sup_year, sup_time))
        for i in new_table:
            if i[1] not in old_table:
                self.cur.execute(f'UPDATE films SET title = \'{i[1]}\' WHERE id = \'{i[0]}\'')
            if i[2] not in old_table:
                self.cur.execute(f'UPDATE films SET year = \'{i[2]}\' WHERE id = \'{i[0]}\'')
            if i[3] not in old_table:
                self.cur.execute(f'UPDATE films SET duration = \'{i[3]}\' WHERE id = \'{i[0]}\'')
        #фиксируем изменения
        self.con.commit()

class Add(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add.ui',self)

        sup_list_two = main.cur.execute('SELECT * FROM genres').fetchall()
        sup_list_two = [i[1] for i in sup_list_two]
        self.new_comboBox.addItems(sup_list_two)

        self.new_row.clicked.connect(self.add_elements)

    def add_elements(self):
        new_genre = self.new_comboBox.currentText()
        new_name = self.new_name.text()
        new_data = self.new_data.text()
        new_time = self.new_time.text()

        request = main.cur.execute(f'SELECT * FROM genres WHERE title = \'{new_genre}\'').fetchall()
        #добавляем новый фильм
        if len(new_genre) != 0:
            main.cur.execute(f'INSERT INTO films(title, duration, genre,year) VALUES(\'{new_name}\',\'{new_time}\',\'{request[0][0]}\',\'{new_data}\')')
        self.new_name.clear()
        self.new_data.clear()
        self.new_time.clear()
        main.con.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    add = Add()
    sys.exit(app.exec_())