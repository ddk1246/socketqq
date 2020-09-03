from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class MainWindow(QMainWindow):

    def __init__(self):
        qfile_window = QFile("ui/mainwindow.ui")
        qfile_window.open(QFile.ReadOnly)
        qfile_window.close()
        self.ui = QUiLoader().load(qfile_window)

        self.ui.SendButton.clicked.connect(self.callback)

    def callback(self):
        return


app = QApplication([])
mainw = MainWindow()
mainw.ui.show()
app.exec_()
