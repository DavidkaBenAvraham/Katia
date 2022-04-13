


from PyQt5 import QtWidgets
import Facebook.ui.QT_login_interface as QT_login_interface
from Facebook.ui.QT_login_interface import Ui_MainWindow as Ui_LoginWindow


class qt_login(QtWidgets.QMainWindow , Ui_LoginWindow):
    def __init__(self , caller , un = '', passwrd = ''):
        '''
        caller - вызывающий класс
        un - username
        passwrd - password
        '''
        super(qt_login, self).__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_startFacebook.clicked.connect(self.pushButton_startFacebook_Clicked)
        self.set_username_password(un , passwrd) 
        self.caller = caller

    def set_username_password(self):
        self.ui.lineEdit_UserName.setText(self.email)
        self.ui.lineEdit_Password.setText(self.passwrd)


    def pushButton_startFacebook_Clicked(self):
        '''
        пересылаю un , passwrd
        в Facebook.log_in()
        '''
        self.caller.un = self.ui.lineEdit_UserName.text()
        self.caller.passwrd = self.ui.lineEdit_Password.text()
        self.caller.log_in(self.caller.un , self.caller.passwrd)
        pass
