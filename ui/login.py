# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(668, 455)
        palette = QPalette()
        pix = QPixmap("./login.jpg")
        pix = pix.scaled(Form.width(), Form.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        Form.setPalette(palette)
        Form.setStyleSheet(u"*{\n"
                           "                font-size:24px;\n"
                           "                font-family:sans-serif;\n"
                           "                }\n"
                           "                #Form{\n"
                           # "                background-image:url(D:/cpp/Py zk/socketqq/ui/login.jpg);\n"
                           # "                background-color:#FAEBD7;\n"
                           "                }\n"
                           "                QFrame{\n"
                           "                background:rgba(0,0,0,0.8);\n"
                           "                border-radius:15px;\n"
                           "                }\n"
                           "                QPushButton{\n"
                           "                background:#03a9f4;\n"
                           "                color:#fff;\n"
                           "                border-radius:15px;\n"
                           "                }\n"
                           "                QLineEdit{\n"
                           "                border-radius:15px;\n"
                           "                color:#03a9f4;\n"
                           "                }\n"
                           "                QLabel{\n"
                           "                color:#fff;\n"
                           "                background:transparent;\n"
                           "                font-size:30px;\n"
                           "                }\n"
                           "            ")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(150, 160, 361, 251))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.loginIP = QLineEdit(self.frame)
        self.loginIP.setObjectName(u"loginIP")
        self.loginIP.setGeometry(QRect(20, 60, 321, 41))
        self.loginPort = QLineEdit(self.frame)
        self.loginPort.setObjectName(u"loginPort")
        self.loginPort.setGeometry(QRect(20, 120, 321, 41))
        self.loginButton = QPushButton(self.frame)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setGeometry(QRect(20, 180, 321, 51))
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 10, 201, 41))
        self.label.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.loginIP.setPlaceholderText(QCoreApplication.translate("Form", u"UserIP", None))
        self.loginPort.setText("")
        self.loginPort.setPlaceholderText(QCoreApplication.translate("Form", u"Port", None))
        self.loginButton.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("Form", u"Login", None))
    # retranslateUi

