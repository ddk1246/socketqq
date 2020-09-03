# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
                           QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(713, 500)
        # if QT_CONFIG(accessibility)
        MainWindow.setAccessibleName(u"QO")
        # endif // QT_CONFIG(accessibility)
        self.actionload = QAction(MainWindow)
        self.actionload.setObjectName(u"actionload")
        self.actionhelp = QAction(MainWindow)
        self.actionhelp.setObjectName(u"actionhelp")
        self.actionabout = QAction(MainWindow)
        self.actionabout.setObjectName(u"actionabout")
        self.actionaddfriend = QAction(MainWindow)
        self.actionaddfriend.setObjectName(u"actionaddfriend")
        self.action_app = QAction(MainWindow)
        self.action_app.setObjectName(u"action_app")
        self.actionexit = QAction(MainWindow)
        self.actionexit.setObjectName(u"actionexit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout_2.addWidget(self.listView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.horizontalLayout.addWidget(self.textEdit)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.ResetButton = QPushButton(self.centralwidget)
        self.ResetButton.setObjectName(u"ResetButton")

        self.verticalLayout_3.addWidget(self.ResetButton)

        self.SendButton = QPushButton(self.centralwidget)
        self.SendButton.setObjectName(u"SendButton")
        self.SendButton.setIconSize(QSize(20, 30))

        self.verticalLayout_3.addWidget(self.SendButton)

        self.SendShortcut = QComboBox(self.centralwidget)
        self.SendShortcut.addItem("")
        self.SendShortcut.addItem("")
        self.SendShortcut.setObjectName(u"SendShortcut")

        self.verticalLayout_3.addWidget(self.SendShortcut)

        self.verticalLayout_3.setStretch(0, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 6)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 713, 26))
        self.menutest = QMenu(self.menubar)
        self.menutest.setObjectName(u"menutest")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menutest.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menutest.addAction(self.actionload)
        self.menutest.addAction(self.actionaddfriend)
        self.menutest.addSeparator()
        self.menutest.addAction(self.actionexit)
        self.menu.addAction(self.actionhelp)
        self.menu.addAction(self.actionabout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionload.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.actionhelp.setText(QCoreApplication.translate("MainWindow", u"QO\u5e2e\u52a9", None))
        self.actionabout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.actionaddfriend.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u597d\u53cb", None))
        self.action_app.setText(QCoreApplication.translate("MainWindow", u"&app", None))
        self.actionexit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.ResetButton.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e", None))
        self.SendButton.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.SendShortcut.setItemText(0, QCoreApplication.translate("MainWindow", u"Ctrl+Enter", None))
        self.SendShortcut.setItemText(1, QCoreApplication.translate("MainWindow", u"Enter", None))

        self.menutest.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

