# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT_Add_Edit_Delete_Message_interface.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(843, 881)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit_Msg = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Msg.setGeometry(QtCore.QRect(20, 50, 381, 441))
        self.textEdit_Msg.setObjectName("textEdit_Msg")
        self.checkBox_RU = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_RU.setGeometry(QtCore.QRect(30, 10, 70, 17))
        self.checkBox_RU.setObjectName("checkBox_RU")
        self.checkBox_HE = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_HE.setGeometry(QtCore.QRect(30, 30, 70, 17))
        self.checkBox_HE.setObjectName("checkBox_HE")
        self.pushButton_OpenFile = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_OpenFile.setGeometry(QtCore.QRect(410, 20, 111, 23))
        self.pushButton_OpenFile.setObjectName("pushButton_OpenFile")
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(410, 50, 321, 441))
        self.label_image.setText("")
        self.label_image.setObjectName("label_image")
        self.pushButton_Save_only = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Save_only.setGeometry(QtCore.QRect(280, 510, 75, 23))
        self.pushButton_Save_only.setObjectName("pushButton_Save_only")
        self.pushButton_Send_only = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Send_only.setGeometry(QtCore.QRect(280, 540, 75, 23))
        self.pushButton_Send_only.setObjectName("pushButton_Send_only")
        self.pushButton_Save_and_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Save_and_send.setGeometry(QtCore.QRect(280, 570, 75, 23))
        self.pushButton_Save_and_send.setObjectName("pushButton_Save_and_send")
        self.checkBox_Send2Facebook = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Send2Facebook.setGeometry(QtCore.QRect(20, 510, 151, 17))
        self.checkBox_Send2Facebook.setObjectName("checkBox_Send2Facebook")
        self.checkBox_Send2Orbita = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Send2Orbita.setGeometry(QtCore.QRect(20, 530, 151, 17))
        self.checkBox_Send2Orbita.setObjectName("checkBox_Send2Orbita")
        self.checkBox_Send2Doska_Objavlenij = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Send2Doska_Objavlenij.setGeometry(QtCore.QRect(20, 550, 151, 17))
        self.checkBox_Send2Doska_Objavlenij.setObjectName("checkBox_Send2Doska_Objavlenij")
        self.checkBox_Send2Calil_co_il = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Send2Calil_co_il.setGeometry(QtCore.QRect(20, 570, 151, 16))
        self.checkBox_Send2Calil_co_il.setObjectName("checkBox_Send2Calil_co_il")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 843, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox_RU.setText(_translate("MainWindow", "RU"))
        self.checkBox_HE.setText(_translate("MainWindow", "HE"))
        self.pushButton_OpenFile.setText(_translate("MainWindow", "Open image file"))
        self.pushButton_Save_only.setText(_translate("MainWindow", "Save Only"))
        self.pushButton_Send_only.setText(_translate("MainWindow", "Send Only"))
        self.pushButton_Save_and_send.setText(_translate("MainWindow", "Save && send"))
        self.checkBox_Send2Facebook.setText(_translate("MainWindow", "Facebook"))
        self.checkBox_Send2Orbita.setText(_translate("MainWindow", "Orbita"))
        self.checkBox_Send2Doska_Objavlenij.setText(_translate("MainWindow", "Doska-objavlenij.com"))
        self.checkBox_Send2Calil_co_il.setText(_translate("MainWindow", "Calil.co.il"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

