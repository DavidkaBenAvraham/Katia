
from PyQt5 import * 
from PyQt5 import QtWidgets
import Facebook.ui.QT_login_interface as QT_login_interface
from Messages.ui.QT_messages_editor_interface import Ui_MainWindow as Ui_MainWindow
import Facebook.db as db

class qt_messages_window(QtWidgets.QMainWindow , Ui_MainWindow):
    def __init__(self ):

        super(qt_messages_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableView.setModel(PandasModel(
            db.get_messages())
                                   )
        
class PandasModel(QtCore.QAbstractTableModel):
    '''
    Class to populate a table view with a pandas dataframe
    '''
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

