from PyQt5 import QtWidgets
from UI.QT_launcher_interface import Ui_Launcher as Ui_Launcher
from Messages.ui.QT_messages_editor_controller import qt_messages_window as qt_messages_window
from Messages.ui.QT_Add_Edit_Delete_Message_controller import qt_messages_add_edit_delete as qt_messages_add_edit_delete

from Morlevi.ui.QT_Mor_main_controller import qt_mor_main_window as qt_mor_main_window

import sys

import Facebook
import Morlevi

from Ini import Ini
import execute_json as jsn
import ExceptionsHandler
from Logging import Log as log


class qt_launher(QtWidgets.QMainWindow , Ui_Launcher):
    def __init__(self ):
        super(qt_launher, self).__init__()
        self.ui = Ui_Launcher()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_messgaes_windows_open.clicked.connect(self.pushButton_messgaes_windows_open_Clicked)
        self.ui.pushButtonAddEditDeleteMessage.clicked.connect(self.pushButtonAddEditDeleteMessage_Clicked)
        self.ui.pushButtonMorLeviLogin.clicked.connect(self.mor_levi)
        self.ui.pushButtonFacebookLogin.clicked.connect(self.facebook)

    def pushButton_messgaes_windows_open_Clicked(self):
        self.messages_window = qt_messages_window()
        self.messages_window.show()
        pass

    def pushButtonAddEditDeleteMessage_Clicked(self):
        self.messages_add_edit_delete_window = qt_messages_add_edit_delete()
        self.messages_add_edit_delete_window.show()
        pass

    def mor_levi(self):
        mor = Morlevi.SiteScraper()
        mor.run()
        self.mor_main_window = qt_mor_main_window()
        self.mor_main_window.set_object_Mor(mor) # передаю инстанс класса Мор 
        self.mor_main_window.show()

        pass
    def facebook(self):
        fb = Facebook.FB()
        fb.run()
        fb.send(lang = '*', from_ROWID = 0 , to_ROWID = 'max')