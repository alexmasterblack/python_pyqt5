import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import html


class HtmlEdit(QMainWindow, html.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_example)
        self.pushButton_2.clicked.connect(self.trans_to_browser)

    def trans_to_browser(self):
        html_code = self.plainTextEdit
        text = html_code.toPlainText()
        self.textBrowser.setText(text)
    
    def print_example(self):
        example = "<body><p><i>Привет</i>, это моя первая программа в Qt Designer!</p><p>Выглядит не особо...</p></body>"
        self.plainTextEdit.insertPlainText(example)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = HtmlEdit()
    form.show()
    sys.exit(app.exec())
