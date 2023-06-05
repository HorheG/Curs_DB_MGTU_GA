import reg_pass
from Frame import route_train

from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem



class route_trainApp(QtWidgets.QMainWindow, route_train.Ui_MainWindow):
    def __init__(self, parent, res, conn):
        super().__init__(parent)
        self.setupUi(self)
        self.res = res
        self.conn = conn
        self.setWindowTitle(self.res[0][1] + ' - '+ self.res[0][2])
        self.resize(1260,300)
        self.pushButton.clicked.connect(self.last_window)
        self.pushButton_2.clicked.connect(self.reg_pass_window)
    
    def reg_pass_window(self):
        self.hide()
        self.reg_pass_window = reg_pass.reg_passApp(self, self.res, self.conn)
        self.reg_pass_window.show()
    
    def last_window(self):
        self.close()
        self.parent().show()

    
    def LoadTrain(self):
        self.model = QStandardItemModel()
        self.model.setColumnCount(10)
        self.model.setRowCount(len(self.res))
        self.model.setHorizontalHeaderLabels(['Поезд','Откуда','Куда','Дата отправления','Время отправления','Дата прибытия',
                                              'Время прибытия','Плацкарт','Купе', 'СВ'])
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.resizeColumnsToContents()
        header = self.tableView.horizontalHeader()
        for i in range(header.count()):
            header.resizeSection(i, header.sectionSizeHint(i))
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                item = QStandardItem(str(self.res[row][column]))
                self.model.setItem(row, column, item)
        self.tableView.setModel(self.model)
        
        
        