from PyQt5 import QtCore

class dbListModel(QtCore.QAbstractListModel):
    def __init__(self, rows, parent=None):
        super(dbListModel, self).__init__(parent)
        self.rows = rows
        self.dataList = []
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.rows)


class dbTableModel(QtCore.QAbstractTableModel):
    def __init__(self, columns, parent=None):
        super(dbTableModel, self).__init__(parent)
        self.columns = columns
        self.dataList = []
    
    def columnsCount(self, parent=QtCore.QModelIndex()):
        return len(self.columns)
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section].title()
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = self.datatable[index.row()]
            column_key = self.columns[index.column()]
            return row[column_key]
        else:
            return None   
