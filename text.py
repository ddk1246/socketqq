from PySide2.QtWidgets import QApplication, QMainWindow, QShortcut, QTextBrowser, QPushButton, QWidget
from PySide2.QtGui import QColor, QKeySequence
from PySide2 import QtCore
from PySide2.QtCore import Signal, QObject
from ui.mainwindow import Ui_MainWindow
from ui.login import Ui_Form
import socket
import threading
import time


class SendSignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    text_print = Signal(QPushButton, str, QColor)
    # 还可以定义其他信号
    # update_table = Signal(str)


class ClearSignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    message_clear = Signal(QPushButton, str, QColor)


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # self.mw=mainwindow

        # self.ui.loginButton.clicked.connect(self.login)

    def loginFunc(self):
        return {'IP': self.ui.loginIP.text(), 'Port': self.ui.loginPort.text()}


class MainWindow(QMainWindow):
    textSignal = Signal(QPushButton, str, QColor)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.child = LoginWindow()

        self.aimIp = '127.0.0.1'  # '10.128.211.162'
        self.aimPort = 7788
        self.hostIp = '127.0.0.1'  # '10.128.230.233'
        self.hostPort = 5566

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket.bind((self.hostIp, self.hostPort))
        self.sendsignal = SendSignals()
        # self.sendsignal22 = Signal(QPushButton, str, QColor) # //test
        self.sendsignal22.connect(self.printToGui)
        self.clearsignal = ClearSignals()
        # 信号与槽
        self.sendsignal.text_print.connect(self.printToGui)
        self.clearsignal.message_clear.connect(self.clearToGui)
        self.ui.SendButton.clicked.connect(self.threadOfSendMessage)
        self.ui.ResetButton.clicked.connect(self.clearSendText)
        self.child.ui.loginButton.clicked.connect(self.childAccept)

        self.child.show()

        tr = threading.Thread(target=self.recvMessage, args=(self.tcp_socket,))
        tr.start()
        self.ShortcutSetting()

    def printToGui(self, object, text, textColor):
        object.setTextColor(QColor(textColor))
        object.append(str(text))

    def clearToGui(self, object, remindMessage, messageColor):
        object.setText('')
        object.setPlaceholderText(str(remindMessage))

    def clearSendText(self):
        self.clearsignal.message_clear.emit(self.ui.textEdit, '', 'black')

    def recvMessage(self, udp_socket, ):
        """接收数据"""
        while True:
            recv_data = udp_socket.recvfrom(1024)
            recv_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            # self.sendsignal.text_print.emit(self.ui.textBrowser, recv_data[1][0] + '  ' + recv_time, 'red')
            # self.sendsignal.text_print.emit(self.ui.textBrowser, '  ' + recv_data[0].decode('gbk'), 'black')
            # print("收到了消息%s:%s" % (str(recv_data[1]), recv_data[0].decode("gbk")))

            self.sendsignal22.emit(self.ui.textBrowser, recv_data[1][0] + '  ' + recv_time, 'red')
            self.sendsignal22.emit(self.ui.textBrowser, '  ' + recv_data[0].decode('gbk'), 'black')

    def threadOfSendMessage(self):
        ts = threading.Thread(target=self.sendMessageTEST)
        ts.start()

    def sendMessageTEST(self):
        info = self.ui.textEdit.toPlainText()
        if (info):
            sendTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            self.sendsignal.text_print.emit(self.ui.textBrowser, self.hostIp + '  ' + sendTime + ' [本地]', '#87CEEB')
            self.sendsignal.text_print.emit(self.ui.textBrowser, '  ' + info, 'black')
            self.clearsignal.message_clear.emit(self.ui.textEdit, '', 'black')
            self.tcp_socket.sendto(info.encode("gbk"), (self.aimIp, self.aimPort))
        else:
            self.clearsignal.message_clear.emit(self.ui.textEdit, '输入不能为空', 'black')

    def sendMessage(self):
        info = self.ui.textEdit.toPlainText()
        if (info):
            sendTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            self.printToGui(self.ui.textBrowser, self.hostIp + '  ' + sendTime, '#87CEEB')
            self.printToGui(self.ui.textBrowser, '  ' + info, 'black')
            self.ui.textEdit.setText('')
            # self.tcp_socket.connect((self.aimIp,self.aimPort))
            self.tcp_socket.sendto(info.encode("gbk"), (self.aimIp, self.aimPort))

        else:
            self.ui.textEdit.setText('输入不能为空')

    # 快捷键设置
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
        self.accept(self.child)
        self.show()
        self.clearToGui(self.child.ui.loginIP, '', 'black')
        self.clearToGui(self.child.ui.loginPort, '', 'black')
        # self.child.ui.loginIP.setText()
        self.child.close()

    # def userLogin(self):
    #
    # def addFriend(self):


def main():
    app = QApplication([])

    mainw = MainWindow()
    mainw.setWindowTitle('QO')
    # mainw.show()

    app.exec_()


if __name__ == '__main__':
    main()
