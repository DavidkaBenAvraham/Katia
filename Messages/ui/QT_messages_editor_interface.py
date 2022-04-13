# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT_messages_editor_interface.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(827, 728)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 430, 791, 192))
        self.tableView.setObjectName("tableView")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 30, 241, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lineEditMsgID = QtWidgets.QLineEdit(self.frame)
        self.lineEditMsgID.setGeometry(QtCore.QRect(50, 30, 51, 20))
        self.lineEditMsgID.setObjectName("lineEditMsgID")
        self.pushButtonFindMsgByMsgID = QtWidgets.QPushButton(self.frame)
        self.pushButtonFindMsgByMsgID.setGeometry(QtCore.QRect(110, 30, 75, 23))
        self.pushButtonFindMsgByMsgID.setObjectName("pushButtonFindMsgByMsgID")
        self.label_MsgID = QtWidgets.QLabel(self.frame)
        self.label_MsgID.setGeometry(QtCore.QRect(50, 10, 47, 13))
        self.label_MsgID.setObjectName("label_MsgID")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 827, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonFindMsgByMsgID.setText(_translate("MainWindow", "Find"))
        self.label_MsgID.setText(_translate("MainWindow", "Msg ID"))

