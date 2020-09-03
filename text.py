from PySide2.QtWidgets import QApplication, QMainWindow, QShortcut, QTextBrowser, QPushButton, QWidget
from PySide2.QtGui import QColor, QKeySequence
from PySide2 import QtCore
from PySide2.QtCore import Signal, QObject, QStringListModel
from ui.mainwindow import Ui_MainWindow
from ui.login import Ui_Form
import socket
import threading
import time


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def loginFunc(self):
        return {'IP': self.ui.loginIP.text(), 'Port': self.ui.loginPort.text()}


class MainWindow(QMainWindow):
    textSendSignal = Signal(QPushButton, str, QColor)
    textClearSignal = Signal(QPushButton, str, QColor)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.input = LoginWindow()

        self.aimIp = '127.0.0.1'  # '10.128.211.162'
        self.aimPort = 7788
        self.hostIp = '127.0.0.1'  # '10.128.230.233'
        self.hostPort = 55666

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket.bind((self.hostIp, self.hostPort))

        # （begin）列表--------
        slm = QStringListModel();  # 创建mode
        self.friendList = []  # 添加的数组数据
        slm.setStringList(self.friendList)  # 将数据设置到model
        self.ui.listView.setModel(slm)  # 绑定 listView 和 model

        # （end）列表--------

        # 信号与槽
        self.textSendSignal.connect(self.printToGui)
        self.textClearSignal.connect(self.clearToGui)

        self.ui.SendButton.clicked.connect(self.threadOfSendMessage)
        self.ui.ResetButton.clicked.connect(self.clearSendText)
        self.input.ui.loginButton.clicked.connect(self.childAccept)
        self.ui.listView.clicked.connect(self.clickedlist)

        self.ui.actionexit.triggered.connect(self.systemQuitFunc)
        self.ui.actionload.triggered.connect(self.userLoginFunc)
        self.ui.actionaddfriend.triggered.connect(self.addFriendFunc)

        self.input.show()
        self.input.close()
        self.input.show()

        self.thr = threading.Thread(target=self.recvMessageFunc, args=(self.tcp_socket,))
        self.thr.start()
        self.ShortcutSetting()

    def systemQuitFunc(self):
        pass  # todo 系统退出

    def clickedlist(self, qModelIndex):
        ip, port = self.friendList[qModelIndex.row()][0], self.friendList[qModelIndex.row()][1]
        self.setAimIP(ip)
        self.setAimPort(port)
        # todo 数据库引入

    def printToGui(self, object, text, textColor):
        object.setTextColor(QColor(textColor))
        object.append(str(text))

    def clearToGui(self, object, remindMessage, messageColor):
        object.setText('')
        object.setPlaceholderText(str(remindMessage))

    def clearSendText(self):
        self.textClearSignal.emit(self.ui.textEdit, '', 'black')

    def threadOfSendMessage(self):
        ts = threading.Thread(target=self.sendMessageFunc)
        ts.start()

    def recvMessageFunc(self, udp_socket, ):
        """接收数据"""
        while True:
            recv_data = udp_socket.recvfrom(1024)
            recv_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            self.textSendSignal.emit(self.ui.textBrowser, recv_data[1][0] + '  ' + recv_time, 'red')
            self.textSendSignal.emit(self.ui.textBrowser, '  ' + recv_data[0].decode('gbk'), 'black')
            # print("收到了消息%s:%s" % (str(recv_data[1]), recv_data[0].decode("gbk")))

    def sendMessageFunc(self):
        info = self.ui.textEdit.toPlainText()
        if (info):
            sendTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            self.textSendSignal.emit(self.ui.textBrowser, self.hostIp + '  ' + sendTime + ' [本地]', '#87CEEB')
            self.textSendSignal.emit(self.ui.textBrowser, '  ' + info, 'black')
            self.textClearSignal.emit(self.ui.textEdit, '', 'black')
            self.tcp_socket.sendto(info.encode("gbk"), (self.aimIp, self.aimPort))
        else:
            self.textClearSignal.emit(self.ui.textEdit, '输入不能为空', 'black')

    # (begin)快捷键设置------------
    def ShortcutSetting(self):
        QShortcut(QKeySequence(self.tr('Ctrl+Q')), self, self.close)
        self.ui.SendButton.setShortcut('ctrl+return')
        self.ui.SendShortcut.currentIndexChanged.connect(self.setSendButtonShortcut)

    def setSendButtonShortcut(self):
        change = self.ui.SendShortcut.currentText()
        if change == 'Ctrl+Enter':
            self.ui.SendButton.setShortcut(change.replace('Enter', 'return'))
        elif change == 'Enter':
            QShortcut(QKeySequence(self.tr('return')), self, self.ui.SendButton.click)
        # todo(wzk) 应实现回车发送功能

    # (end)快捷键设置------------

    def setHostIP(self, ipstr):
        self.hostIp = str(ipstr)

    def setHostPort(self, portstr):
        self.hostPort = int(portstr)

    def setAimIP(self, ipstr):
        self.aimIp = str(ipstr)

    def setAimPort(self, portstr):
        self.aimPort = int(portstr)

    def accept(self, object):
        self.setHostIP(object.ui.loginIP.text())
        self.setHostPort(object.ui.loginPort.text())

    def childAccept(self):
        self.accept(self.input)
        self.show()
        self.clearToGui(self.input.ui.loginIP, '', 'black')
        self.clearToGui(self.input.ui.loginPort, '', 'black')
        # self.child.ui.loginIP.setText()
        self.input.close()

    def userLoginFunc(self):
        self.input.ui.label.setText('Login')
        self.input.ui.loginButton.setText('登录')
        self.input.ui.loginIP.setPlaceholderText('UserIP')
        self.input.ui.loginPort.setPlaceholderText('Port')

        # self.input.ui.loginPort.text()

        self.input.show()
        self.input.ui.loginButton.clicked.connect(self.loginAccept)

    def loginAccept(self):
        self.input = LoginWindow()
        self.setHostIP(self.input.ui.loginIP.text())
        self.setHostPort(self.input.ui.loginPort.text())
        self.input.close()

    def addFriendFunc(self):
        self.input = LoginWindow()
        self.input.ui.label.setText('Add Friend')
        self.input.ui.loginButton.setText('添加')
        self.input.ui.loginIP.setPlaceholderText('FriendIP')
        self.input.ui.loginPort.setPlaceholderText('Port')
        self.input.show()
        self.input.ui.loginButton.clicked.connect(self.friendAccept)

    def friendAccept(self):
        ip, port = self.input.ui.loginIP.text(), self.input.ui.loginPort.text()
        print("23330", ip, '\n', port)
        self.setAimIP(ip)
        self.setAimPort(port)
        self.friendList.append([ip, port])

        slm = QStringListModel();  # 创建mode
        slm.setStringList(self.friendList)  # 将数据设置到model
        self.ui.listView.setModel(slm)  # 绑定 listView 和 model

        self.input.close()

    def deleteFriendFunc(self):
        pass  # todo 删除好友函数


def main():
    app = QApplication([])

    mainw = MainWindow()
    mainw.setWindowTitle('QO')
    # mainw.show()

    app.exec_()


if __name__ == '__main__':
    main()
