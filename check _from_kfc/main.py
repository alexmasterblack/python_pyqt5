import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit
import kfc


class KFC(QMainWindow, kfc.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.goods = [
            ('Чизбургер с Луком', 74.0), ('Шефбургер Джуниор', 109.0), ('Баскет L', 709.0),
            ('Баскет 5 ножек', 384.0), ('Твистер Оригинальный', 174.0), ('Боксмастер', 214.0)
        ]

        self.buttons = [
            (self.spin_1, self.check_1), (self.spin_2, self.check_2), (self.spin_3, self.check_3),
            (self.spin_4, self.check_4), (self.spin_5, self.check_5), (self.spin_6, self.check_6)
        ]

        self.check_1.stateChanged.connect(
            lambda: self.spin_1.setEnabled(self.check_1.isChecked()))
        self.check_2.stateChanged.connect(
            lambda: self.spin_2.setEnabled(self.check_2.isChecked()))
        self.check_3.stateChanged.connect(
            lambda: self.spin_3.setEnabled(self.check_3.isChecked()))
        self.check_4.stateChanged.connect(
            lambda: self.spin_4.setEnabled(self.check_4.isChecked()))
        self.check_5.stateChanged.connect(
            lambda: self.spin_5.setEnabled(self.check_5.isChecked()))
        self.check_6.stateChanged.connect(
            lambda: self.spin_6.setEnabled(self.check_6.isChecked()))

        self.tabWidget.currentChanged.connect(self.print_result)

    def print_result(self):
        if self.tabWidget.currentIndex() == 1:
            self.result = 0
            self.print.clear()
            for i in range(len(self.buttons)):
                if self.buttons[i][1].isChecked():
                    self.text = self.goods[i][0] + " - " + str(self.goods[i][1]) + " x " + str(self.buttons[i][0].value()) + " - " + str(self.goods[i][1] * self.buttons[i][0].value()) + "\n"
                    self.print.insertPlainText(self.text)
                    self.result += self.goods[i][1] * self.buttons[i][0].value()
            self.print.insertPlainText("\n")
            self.print.insertPlainText("К оплате: " + str(self.result) + " ₽")
                
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = KFC()
    form.show()
    sys.exit(app.exec())