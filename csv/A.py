import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout
import csv


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.loadUI()
        self.loadTable('students.csv')

    def loadUI(self):
        self.setGeometry(100, 100, 450, 300)
        self.lay = QHBoxLayout()
        self.table = QTableWidget()
        self.lay.addWidget(self.table)
        self.setLayout(self.lay)

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            # считаем информацию из таблицы
            reader = csv.reader(csvfile, delimiter=',')
            title = next(reader)
            self.table.setColumnCount(len(title))
            self.table.setHorizontalHeaderLabels(title)
            self.table.setRowCount(0)

            for index, row in enumerate(reader):
                self.table.setRowCount(self.table.rowCount() + 1)

                rating = 0
                for cell in range(2, 10, 1):
                    rating = rating + float(row[cell].replace(',', '.')) / 8

                color = '#FFFFFF'
                if rating >= 95:
                    color = '#9CF071'
                elif rating < 95 and rating >= 80:
                    color = '#F9F78F'
                elif rating < 80 and rating >= 60:
                    color = '#F07A71'

                for j, elem in enumerate(row):
                    # добавляем элемент
                    self.table.setItem(index, j, QTableWidgetItem(elem))
                    # красим
                    self.table.item(index, j).setBackground(
                        QtGui.QColor(color))
                    # QtGui.QColor принимает цвет

        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.exit(app.exec())
