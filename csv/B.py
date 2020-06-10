import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QTableWidgetItem


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('B.ui', self)
        self.con = sqlite3.connect('films.db')
        self.cur = self.con.cursor()

        self.search.clicked.connect(self.fout)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ['Название', 'Год', 'Длительность'])
        # растягиваю таблицку по размеру виджета
        self.table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)

    def fout(self):
        request = self.input.text()
        self.table.setRowCount(0)
        #смотрим в таблицу гендеров, если ли такие жанры
        result = self.cur.execute(f'SELECT * FROM genres WHERE title = \'{request}\'').fetchall()
        if len(result) != 0:
            #так как айди таблица жанров связано с таблицей фильмов с гендером, то теперь вывожу все ответы
            all_result = self.cur.execute(f'SELECT * FROM Films WHERE genre = \'{result[0][0]}\'').fetchmany(150)

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
