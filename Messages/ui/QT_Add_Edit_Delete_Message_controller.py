from PyQt5 import * 
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from Messages.ui.QT_Add_Edit_Delete_Message_interface import Ui_MainWindow as ui_Add_Edit_Delete_Message
import Facebook.db as db

class qt_messages_add_edit_delete(QtWidgets.QMainWindow , ui_Add_Edit_Delete_Message):
    def __init__(self):
        super(qt_messages_add_edit_delete, self).__init__()
        self.ui = ui_Add_Edit_Delete_Message()
        self.ui.setupUi(self)


        #https://pythonspot.com/pyqt5-file-dialog/
        self.ui.pushButton_OpenFile.clicked.connect(self.openFileNameDialog)


        #https://ru.stackoverflow.com/questions/697148/%D0%92%D0%B8%D0%B4%D0%B6%D0%B5%D1%82-%D0%B4%D0%BB%D1%8F-%D0%BE%D1%82%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8-%D0%B2-pyqt-%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D1%83-%D0%B8%D0%B7-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0
        #self.ui.label_image

        self.ui.pushButton_Save_only.clicked.connect(self.save_message)
        self.ui.pushButton_Send_only.clicked.connect(self.send_message)
        self.ui.pushButton_Save_and_send.clicked.connect(self.save_and_send)

        '''
        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()
        '''
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.load_image(self.fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            self.print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.print(fileName)

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        self.ui.label_image.setPixmap(pixmap)
        self.ui.label_image.resize(pixmap.width(), pixmap.height())

    def save_message(self):
        pass
    def send_message(self):
        pass
    def save_and_send(self):
        self.save_message()
        self.send_message()
        pass