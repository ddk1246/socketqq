# from PySide2.QtWidgets import QApplication, QMainWindow, QShortcut, QTextBrowser, QPushButton, QWidget,QMenu
# from PySide2.QtGui import QColor, QKeySequence,QCursor
# from PySide2 import QtCore
# from PySide2.QtCore import Signal, QObject, QStringListModel,QPoint
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ui.mainwindow import Ui_MainWindow
from ui.login import Ui_Form
import socket
import threading
import time
import numpy as np
import re


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.loginButton.setShortcut('enter')
        # self.ui.loginButton.setShortcut('ctrl+return')

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
        self.hostIp = str(localIP())  # 10.128.230.233
        self.hostPort = 5566

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket.bind((self.hostIp, self.hostPort))

        # （begin）列表--------
        # 列表加载
        slm = QStringListModel();  # 创建mode
        self.friendList = [['127.0.0.1', 7788], ['127.0.0.1', 7888], ['127.0.0.1', 8888]]  # 添加的数组数据
        slm.setStringList(np.array(self.friendList)[:, 0])  # 将数据设置到model

        # 列表右键拓展
        self.ui.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listView.customContextMenuRequested[QPoint].connect(self.listWidgetContext)

        self.ui.listView.setModel(slm)  # 绑定 listView 和 model
        # （end）列表--------

        # 信号与槽
        self.textSendSignal.connect(self.printToGui)
        self.textClearSignal.connect(self.clearToGui)

        self.ui.SendButton.clicked.connect(self.threadOfSendMessage)
        self.ui.ResetButton.clicked.connect(self.clearSendText)
        # self.input.ui.loginButton.clicked.connect(self.childAccept)
        self.ui.listView.clicked.connect(self.clickedlist)

        self.ui.actionexit.triggered.connect(self.systemQuitFunc)
        self.ui.actionload.triggered.connect(self.userLoginFunc)
        self.ui.actionaddfriend.triggered.connect(self.addFriendFunc)
        self.ui.actionabout.triggered.connect(self.programAbout)
        self.ui.actionhelp.triggered.connect(self.programHelp)

        # 监听窗口线程
        self.thr = threading.Thread(target=self.recvMessageFunc, args=(self.tcp_socket,))
        self.thr.daemon = 1
        self.thr.start()

        self.ShortcutSetting()

        self.userLoginFunc()

    def programHelp(self):
        choice = QMessageBox.information(
            self,
            '快捷键说明',
            '  Ctrl+Q    :  退出\n'
            'Ctrl+Enter  :  发送', QMessageBox.Yes, QMessageBox.Yes)

    def programAbout(self):
        choice = QMessageBox.information(
            self,
            '关于',
            '开发人员 ：王赞昆   许益豪', QMessageBox.Yes, QMessageBox.Yes)

    def listWidgetContext(self, point):
        listRightMenu = QMenu(self.ui.listView)

        addAction = QAction(u"添加", self, triggered=self.addFriendFunc)  # 也可以指定自定义对象事件
        alterAction = QAction(u"修改", self, triggered=lambda: self.alterFriendFunc())  # 也可以指定自定义对象事件
        removeAction = QAction(u"删除", self, triggered=lambda: self.deleteFriendFunc())  # 也可以指定自定义对象事件
        # //or  removeAction.triggered.connect(lambda:self.deleteFriendFunc(point))
        listRightMenu.addAction(addAction)
        listRightMenu.addAction(alterAction)
        listRightMenu.addAction(removeAction)
        listRightMenu.exec_(QCursor.pos())

    def systemQuitFunc(self):
        QCoreApplication.instance().quit()
        #

    def clickedlist(self, qModelIndex):
        ip, port = self.friendList[qModelIndex.row()][0], self.friendList[qModelIndex.row()][1]
        self.setAimIP(ip)
        self.setAimPort(port)
        self.statusbarShow('Login IP: ' + str(self.hostIp) + '    Port:' + str(self.hostPort) +
                           '        Aim IP: ' + str(ip) + '    Port:' + str(port))
        print("clicked", ip, port)
        # todo 数据库引入聊天内容

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
            try:
                self.tcp_socket.sendto(info.encode("gbk"), (self.aimIp, self.aimPort))
            except Exception as e:
                self.statusbarShow(e)
            except OSError  as osE:
                self.statusbarShow(osE)
            except:
                pass
        else:
            self.textClearSignal.emit(self.ui.textEdit, '输入不能为空', 'black')

    # (begin) 快捷键设置------------
    def ShortcutSetting(self):
        QShortcut(QKeySequence(self.tr('Ctrl+Q')), self, self.close)
        self.ui.SendButton.setShortcut('ctrl+return')
        self.ui.SendShortcut.currentIndexChanged.connect(self.setSendButtonShortcut)
        self.input.ui.loginButton.setShortcut('Enter')

    def setSendButtonShortcut(self):
        change = self.ui.SendShortcut.currentText()
        if change == 'Ctrl+Enter':
            self.ui.SendButton.setShortcut(change.replace('Enter', 'return'))
        elif change == 'Enter':
            QShortcut(QKeySequence(self.tr('return')), self, self.ui.SendButton.click)
        # todo(wzk) 应实现回车发送功能

    #  (end)  快捷键设置------------

    def setHostIP(self, ipstr):
        self.hostIp = str(ipstr)

    def setHostPort(self, portstr):
        self.hostPort = int(portstr)

    def setAimIP(self, ipstr):
        self.aimIp = str(ipstr)

    def setAimPort(self, portstr):
        self.aimPort = int(portstr)

    # (begin)  old ========
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

    #  (end)  old ========

    def statusbarShow(self, string):
        self.ui.statusbar.showMessage(string, 0)

    # (begin) 用户登录 ========
    def userLoginFunc(self):
        self.input = LoginWindow()
        self.input.ui.label.setText('Login')
        self.input.ui.loginButton.setText('登录')
        self.input.ui.loginIP.setPlaceholderText('UserIP')
        self.input.ui.loginIP.setText(self.hostIp)
        self.input.ui.loginPort.setPlaceholderText('Port')
        self.input.ui.loginPort.setText(str(self.hostPort))

        self.input.ui.loginButton.setShortcut('Enter')

        self.input.show()
        self.input.ui.loginButton.clicked.connect(self.loginAccept)

    def loginAccept(self):
        ip, port = self.input.ui.loginIP.text(), self.input.ui.loginPort.text()
        if not isIP(ip) or not isPort(port):
            self.input.close()
            QMessageBox.warning(self, '警告', '请输入正确的IP和端口', QMessageBox.Yes, QMessageBox.Yes)
            self.userLoginFunc()
            return
        self.setHostIP(ip)
        self.setHostPort(port)
        self.input.close()

        self.show()
        # print(self.isActiveWindow()) #判断主窗口是否激活
        self.statusbarShow('Login IP: ' + str(ip) + '    Port:' + str(port))

    #  (end)  用户登录 ========

    # (begin) 增加好友功能 ========
    def addFriendFunc(self):
        self.input = LoginWindow()
        self.input.ui.label.setText('Add Friend')
        self.input.ui.loginButton.setText('添加')
        self.input.ui.loginButton.colorCount()
        self.input.ui.loginIP.setPlaceholderText('FriendIP')
        self.input.ui.loginPort.setPlaceholderText('Port')
        self.input.ui.loginButton.setShortcut('Enter')

        self.input.show()
        self.input.ui.loginButton.clicked.connect(self.addFriendAccept)

    def addFriendAccept(self):
        ip, port = self.input.ui.loginIP.text(), self.input.ui.loginPort.text()
        if not isIP(ip) or not isPort(port):
            self.input.close()
            QMessageBox.warning(self, '警告', '请输入正确的IP和端口', QMessageBox.Yes, QMessageBox.Yes)
            self.addFriendFunc()
            return
        print("addFriendAccept", ip, port)
        self.friendList.append([ip, port])
        print('frindList:', self.friendList)
        self.setAimIP(ip)
        self.setAimPort(port)

        itemmodel = self.ui.listView.model()  # 取数据存储数据条数
        count = itemmodel.rowCount()  # count为列表单项的总数
        selectindex = self.ui.listView.currentIndex()  # 取当前选择的数据项位置

        Pos = count  # 当前没有选择则插入到最后位置
        itemmodel.insertRow(Pos)  # 执行插入位置列表项元素扩充
        index = itemmodel.index(Pos, 0)  # 取插入位置的元素项   #todo 也许是(行，列)
        stritem = ip  # 设置插入内容
        itemmodel.setData(index, stritem, Qt.DisplayRole)  # 将内容更新到插入位置

        self.input.close()

    #  (end)  增加好友功能 ========

    # (begin) 修改好友功能 ========
    def alterFriendFunc(self):
        selectindex = self.ui.listView.currentIndex()
        pos = selectindex.row()
        [ip, port] = self.friendList[pos]
        self.input = LoginWindow()
        self.input.ui.label.setText('Alter Friend')
        self.input.ui.loginButton.setText('修改')
        self.input.ui.loginButton.colorCount()
        self.input.ui.loginIP.setText(ip)
        self.input.ui.loginPort.setText(str(port))
        self.input.ui.loginButton.setShortcut('Enter')

        self.input.show()
        self.input.ui.loginButton.clicked.connect(lambda: self.alterFriendAccept(pos))

    def alterFriendAccept(self, Pos):
        ip, port = self.input.ui.loginIP.text(), self.input.ui.loginPort.text()
        if not isIP(ip) or not isPort(port):
            self.input.close()
            QMessageBox.warning(self, '警告', '请输入正确的IP和端口', QMessageBox.Yes, QMessageBox.Yes)
            self.alterFriendFunc()
            return
        self.friendList[Pos] = [ip, port]

        itemmodel = self.ui.listView.model()
        index = itemmodel.index(Pos, 0)  # 取插入位置的元素项   #todo 也许是(行，列)
        stritem = ip  # 设置插入内容
        itemmodel.setData(index, stritem, Qt.DisplayRole)  # 将内容更新到插入位置

        self.input.close()

    #  (end)  修改好友功能 ========

    # (begin) 删除好友功能 ========
    def deleteFriendFunc(self):
        selectindex = self.ui.listView.currentIndex()
        # selectedindexes = self.ui.listView.selectedIndexes() #todo 函数含义是什么？
        itemmodel = self.ui.listView.model()

        if selectindex.isValid():
            Pos = selectindex.row()
            print("pos=", Pos)  # 取当前选择的数据项位置的顺序索引
        else:
            print("空选项")
            return
        if Pos == 0:
            return
        itemmodel.removeRow(Pos)
        self.friendList.pop(Pos)

        # self.ui.listView.removeItemWidget(self.ui.listView.takeItem(self.ui.listView.row(item)))
        # todo 注释函数和含义

    #  (end)  删除好友功能 ========

    # 测试函数 ========
    def testprint(self):
        print("in test")


def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


def isPort(num):
    return str(num).isdigit()


def localIP():
    hostname = socket.gethostname()
    print("Host name: %s" % hostname)
    sysinfo = socket.gethostbyname_ex(hostname)
    ip_addr = sysinfo[2]
    return ip_addr[-1]


def main():
    app = QApplication([])

    mainw = MainWindow()
    mainw.setWindowTitle('QO')
    # mainw.show()

    app.exec_()


if __name__ == '__main__':
    main()
