import sys
from PyQt5.QtWidgets import QWidget, QApplication, QListView, QDesktopWidget, QHBoxLayout, QMenu
from PyQt5.QtCore import QStringListModel, QPoint
from PyQt5.QtGui import QCursor


class ListMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print("init ui")
        self.list = QListView(self)
        self.list.setContextMenuPolicy(3)
        self.list.customContextMenuRequested[QPoint].connect(self.listWidgetContext)
        lst = ['a', 'b', 'c']
        model = QStringListModel()
        model.setStringList(lst)
        self.list.setModel(model)
        hlayout = QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(self.list, 18)
        hlayout.addStretch(1)
        self.setLayout(hlayout)
        self.setGeometry(300, 300, 300, 300)
        self.center()

    def listWidgetContext(self, point):
        popMenu = QMenu()
        popMenu.addAction("添加")
        popMenu.addAction("修改")
        popMenu.addAction("删除")
        popMenu.exec_(QCursor.pos())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lm = ListMenu()
    lm.show()
    sys.exit(app.exec_())
