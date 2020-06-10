import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QTableWidgetItem


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('D.ui', self)
        self.con = sqlite3.connect('films.db')
        self.cur = self.con.cursor()

        sup_list = self.cur.execute('SELECT * FROM genres').fetchall()
        sup_list = [i[1] for i in sup_list]
        self.comboBox.addItems(sup_list)

        self.search_one.clicked.connect(self.find_all)
        self.search_two.clicked.connect(self.find_name)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ['Название', 'Год', 'Длительность'])

        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def find_name(self):
        name = self.name.text()
        result = self.cur.execute(f'SELECT * FROM Films WHERE Title like \'%{name}%\'').fetchmany(150)
        self.fout(result)


    def find_all(self):
        data = self.data.text()
        time = self.time.text()
        genre = self.comboBox.currentText()

        all_result = ''
        if genre == 'Не выбрано':
            if data and time:
                all_result = f'SELECT * FROM Films WHERE year = \'{data}\' AND duration = \'{time}\''
            if data and not time:
                all_result = f'SELECT * FROM Films WHERE year = \'{data}\''
            if time and not data:
                all_result = f'SELECT * FROM Films WHERE duration = \'{time}\''
            if not time and not data:
                all_result = f'SELECT * FROM Films'
        else:
            result = self.cur.execute(f'SELECT * FROM genres WHERE title = \'{genre}\'').fetchall()
            all_result = f'SELECT * FROM Films WHERE genre = \'{result[0][0]}\''
            if time:
                all_result += f' AND duration = \'{time}\''
            if data:
                all_result += f' AND year = \'{data}\''
        
        self.fout(self.cur.execute(all_result).fetchmany(150))

    def fout(self, all_result):
        self.table.setRowCount(0)
        for index, elements in enumerate(all_result):
            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(index, 0, QTableWidgetItem(elements[1]))
            self.table.setItem(index, 1, QTableWidgetItem(str(elements[2])))
            self.table.setItem(index, 2, QTableWidgetItem(str(elements[4])))

        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec_())