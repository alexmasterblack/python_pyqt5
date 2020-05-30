import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import calculator

class Calculator(QMainWindow, calculator.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_0.clicked.connect(lambda: self.plainTextEdit.insertPlainText("0"))
        self.pushButton_1.clicked.connect(lambda: self.plainTextEdit.insertPlainText("1"))
        self.pushButton_2.clicked.connect(lambda: self.plainTextEdit.insertPlainText("2"))
        self.pushButton_3.clicked.connect(lambda: self.plainTextEdit.insertPlainText("3"))
        self.pushButton_4.clicked.connect(lambda: self.plainTextEdit.insertPlainText("4"))
        self.pushButton_5.clicked.connect(lambda: self.plainTextEdit.insertPlainText("5"))
        self.pushButton_6.clicked.connect(lambda: self.plainTextEdit.insertPlainText("6"))
        self.pushButton_7.clicked.connect(lambda: self.plainTextEdit.insertPlainText("7"))
        self.pushButton_8.clicked.connect(lambda: self.plainTextEdit.insertPlainText("8"))
        self.pushButton_9.clicked.connect(lambda: self.plainTextEdit.insertPlainText("9"))
        self.pushButton_point.clicked.connect(lambda: self.plainTextEdit.insertPlainText("."))
        self.pushButton_left.clicked.connect(lambda: self.plainTextEdit.insertPlainText("("))
        self.pushButton_right.clicked.connect(lambda: self.plainTextEdit.insertPlainText(")"))
        self.pushButton_add.clicked.connect(lambda: self.plainTextEdit.insertPlainText("+"))
        self.pushButton_sub.clicked.connect(lambda: self.plainTextEdit.insertPlainText("-"))
        self.pushButton_mul.clicked.connect(lambda: self.plainTextEdit.insertPlainText("*"))
        self.pushButton_div.clicked.connect(lambda: self.plainTextEdit.insertPlainText("/"))
        self.pushButton_del.clicked.connect(lambda: self.plainTextEdit.textCursor().deletePreviousChar())
        self.pushButton_c.clicked.connect(lambda: self.plainTextEdit.clear())
        self.pushButton_eq.clicked.connect(self.Equal)

    def Equal(self):
        thing = self.plainTextEdit.toPlainText()
        self.plainTextEdit.clear()
        try:
            result = str(eval(thing))
            self.plainTextEdit.insertPlainText(result)
        except Exception:
            self.plainTextEdit.insertPlainText("Неправильный ввод!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Calculator()
    form.show()
    sys.exit(app.exec())