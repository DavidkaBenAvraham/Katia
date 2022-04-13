# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT_launcher_interface.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Launcher(object):
    def setupUi(self, Launcher):
        Launcher.setObjectName("Launcher")
        Launcher.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Launcher)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_messgaes_windows_open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_messgaes_windows_open.setGeometry(QtCore.QRect(220, 20, 211, 51))
        self.pushButton_messgaes_windows_open.setObjectName("pushButton_messgaes_windows_open")
        self.pushButtonFacebookLogin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonFacebookLogin.setGeometry(QtCore.QRect(10, 20, 211, 51))
        self.pushButtonFacebookLogin.setObjectName("pushButtonFacebookLogin")
        self.pushButtonMorLeviLogin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonMorLeviLogin.setGeometry(QtCore.QRect(10, 70, 211, 51))
        self.pushButtonMorLeviLogin.setObjectName("pushButtonMorLeviLogin")
        self.pushButtonSendOnMessageRightNow = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSendOnMessageRightNow.setGeometry(QtCore.QRect(220, 120, 211, 51))
        self.pushButtonSendOnMessageRightNow.setObjectName("pushButtonSendOnMessageRightNow")
        self.pushButtonAddEditDeleteMessage = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAddEditDeleteMessage.setGeometry(QtCore.QRect(220, 70, 211, 51))
        self.pushButtonAddEditDeleteMessage.setObjectName("pushButtonAddEditDeleteMessage")
        Launcher.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Launcher)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Launcher.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Launcher)
        self.statusbar.setObjectName("statusbar")
        Launcher.setStatusBar(self.statusbar)

        self.retranslateUi(Launcher)
        QtCore.QMetaObject.connectSlotsByName(Launcher)

    def retranslateUi(self, Launcher):
        _translate = QtCore.QCoreApplication.translate
        Launcher.setWindowTitle(_translate("Launcher", "MainWindow"))
        self.pushButton_messgaes_windows_open.setText(_translate("Launcher", "Messages table"))
        self.pushButtonFacebookLogin.setText(_translate("Launcher", "Facebook login"))
        self.pushButtonMorLeviLogin.setText(_translate("Launcher", "Morlevi login"))
        self.pushButtonSendOnMessageRightNow.setText(_translate("Launcher", "Send messages now!"))
        self.pushButtonAddEditDeleteMessage.setText(_translate("Launcher", "Add Delete Edit Message"))

