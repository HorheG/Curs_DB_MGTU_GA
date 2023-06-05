from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from Frame import reg_pass
import Save_pdf

class reg_passApp(QtWidgets.QMainWindow, reg_pass.Ui_MainWindow):
    def __init__(self, parent, res, conn):
        super().__init__(parent)
        self.setupUi(self)
        self.res = res
        self.conn = conn
        self.widgets = [self.comboBox, self.comboBox_2, self.comboBox_4, self.lineEdit_2, self.lineEdit_3,self.lineEdit_4,self.lineEdit,
                        self.lineEdit_5,self.lineEdit_6,self.lineEdit_7,self.lineEdit_8,self.lineEdit_9,self.lineEdit_10,
                        self.dateEdit, self.comboBox_3, self.lineEdit_11,self.lineEdit_12]
        self.settings_window()
        self.comboBox.currentIndexChanged.connect(self.comboBox_Train)
        self.comboBox_2.currentIndexChanged.connect(self.comboBox_price)
        self.pushButton.clicked.connect(self.regist)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.editingFinished.connect(self.update_price)
        
    
    def comboBox_Train(self):
        selected_index = self.comboBox.currentIndex()
        self.lineEdit_2.setText(self.res[selected_index][1])
        self.lineEdit_3.setText(self.res[selected_index][3])
        self.lineEdit_4.setText(self.res[selected_index][4])
        self.lineEdit.setText(self.res[selected_index][2])
        self.lineEdit_5.setText(self.res[selected_index][5])
        self.lineEdit_6.setText(self.res[selected_index][6])
        
    def comboBox_price(self):
        selected_index_train = self.comboBox.currentIndex()
        selected_index_vag = self.comboBox_2.currentIndex()

        if selected_index_vag == 0:
            self.lineEdit_7.setText(str(self.res[selected_index_train][-4]))
            self.comboBox_4.setEnabled(True)
        elif selected_index_vag == 1:
            self.lineEdit_7.setText(str(self.res[selected_index_train][-3]))
            self.comboBox_4.setEnabled(True)
        else:
            self.lineEdit_7.setText(str(self.res[selected_index_train][-2]))
            self.comboBox_4.setEnabled(False)
            self.comboBox_4.setCurrentText('Нижнее')
    
    def settings_window(self):
        
        for i in self.res:
            self.comboBox.addItem(i[0])
        self.lineEdit_2.setText(self.res[0][1])
        self.lineEdit_3.setText(self.res[0][3])
        self.lineEdit_4.setText(self.res[0][4])
        self.lineEdit.setText(self.res[0][2])
        self.lineEdit_5.setText(self.res[0][5])
        self.lineEdit_6.setText(self.res[0][6])
        self.lineEdit_7.setText(str(self.res[0][-3]))
        self.comboBox_2.addItems(['Плацкарт','Купе','СВ'])
        self.comboBox_4.addItems(['Верхнее','Нижнее'])
        
        curs = self.conn.cursor()
        curs.execute('select * from TypeDoc')
        for row in curs:
            self.comboBox_3.addItem(row[1])
    
    def regist(self):
        res = self.collect_widget_text()
        curs = self.conn.cursor()
        ID_doc = curs.execute("""select * from TypeDoc where Name= ? """,(res[-3])).fetchone()[0]

        query1 = """
                INSERT INTO Passanger(Surname, Name, Patronymic, Birthday, ID_typeDoc, Series, Number)
                            Values(?, ? ,? ,CONVERT(DATE, ?, 104), ?, ?, ?)
                """ 
        query2 = """
                INSERT INTO Tikket(ID_train, ID_vag, ID_passanger, ID_cashier, firstStation, LastStation, price)
                            Values(?,?,?,?,?,?,?)
                """
        
        curs.execute(query1, (res[-7], res[-6],res[-5], res[-4], ID_doc, res[-2], res[-1]))
        curs.commit()
        data = self.get_data()
        curs.execute(query2, (self.res[self.comboBox.currentIndex()][-1], data[0], data[1], data[2], res[3], res[6], res[9]) )
        curs.commit()
        curs.close()

        Save_pdf.save_billet(res)
        self.close_window()
    
    def get_data(self):
        result = []
        curs = self.conn.cursor()
        curs.execute("""
                     Select Vag.ID from Vag
                     Join TypeVag ON TypeVag.ID = Vag.IdTypeVag
                     Join TypeSeats ON TypeSeats.ID = Vag.IdTypeSeats
                     where TypeVag.Name = ? and TypeSeats.Name = ?
                     """,(self.comboBox_2.currentText(), self.comboBox_4.currentText()) 
                     )
        result.append(curs.fetchone()[0])
        curs.execute("""
                    SELECT TOP 1 ID FROM Passanger ORDER BY ID DESC
                     """)
        result.append(curs.fetchone()[0])
        
        curs.execute("SELECT SYSTEM_USER")
        username = curs.fetchone()[0]
        curs.execute('Select ID from Cashier where Surname = ?', (username))
        result.append(curs.fetchone()[0])
        curs.close()
        
        return result
        
    def collect_widget_text(self):
        text_list = []
        for widget in self.widgets:
            if isinstance(widget, QtWidgets.QLineEdit):
                text_list.append(widget.text())
            elif isinstance(widget, QtWidgets.QComboBox):
                text_list.append(widget.currentText())
            else:text_list.append(widget.text())
        return text_list
    
    def close_window(self):
        self.close()
        self.parent().parent().show()
    
    def update_price(self):
        cure_date = QDate.currentDate()
        input_date = self.dateEdit.date()
        age = cure_date.year() - input_date.year()
        if age < 14:
            self.comboBox_3.setCurrentIndex(1)
            self.comboBox_3.setEnabled(False)
        else: 
            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_3.setEnabled(True)
        if age <= 6:
            selected_index_train = self.comboBox.currentIndex()
            selected_index_vag = self.comboBox_2.currentIndex()
            
            if selected_index_vag == 0:
                curr_price = float(self.res[selected_index_train][-4])
                self.lineEdit_7.setText(str(curr_price * 0.5))
            elif selected_index_vag == 1:
                curr_price = float(self.res[selected_index_train][-3])
                self.lineEdit_7.setText(str(curr_price * 0.5))
            else:
                curr_price = float(self.res[selected_index_train][-2])
                self.lineEdit_7.setText(str(curr_price * 0.5))
        else:
            self.lineEdit_7.setText(str(self.res[0][-3]))
            