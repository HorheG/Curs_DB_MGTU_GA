from Frame_operator import operarot_window
import pyodbc
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QDate

class operator_app(QtWidgets.QMainWindow, operarot_window.Ui_MainWindow):
    def __init__(self, conn):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.graph_settings()
        self.Route_settings()
        self.block_buttons()
        self.train_settings()
        self.comboBox_4.currentIndexChanged.connect(self.graph_combobox_setings)
        self.comboBox.currentIndexChanged.connect(self.route_combobox_settings)
        self.comboBox_2.currentIndexChanged.connect(self.route_combobox_2_settings)
        self.comboBox_3.currentIndexChanged.connect(self.train_combobox_settings)
        
        self.tabWidget.currentChanged.connect(self.block_buttons)
        
        self.pushButton_7.clicked.connect(self.button_update)
        self.pushButton_8.clicked.connect(self.button_insert)
        self.pushButton_10.clicked.connect(self.button_clear)
        
    #Обработка окна ГРАФ*******************************************************************
    
    def graph_settings(self):
        curs = self.conn.cursor()
        res = curs.execute('Select * from Schedule').fetchall()
        curs.close()
        for i in res:
            self.comboBox_4.addItem(str(i[0]))
            self.comboBox.addItem(str(i[0]))
            self.comboBox_3.addItem(str(i[0]))
        self.lineEdit.setText(res[0][1])
        self.lineEdit_2.setText(res[0][2])
        self.lineEdit_3.setText(res[0][3])
        self.lineEdit_4.setText(str(res[0][4])[:-2])
        self.lineEdit_5.setText(str(res[0][5]))
        
    def graph_combobox_setings(self):
        selected_index = self.comboBox_4.currentText()
        curs = self.conn.cursor()
        res = curs.execute('Select * from Schedule Where ID = ?', (selected_index)).fetchone()
        curs.close()
        self.lineEdit.setText(res[1])
        self.lineEdit_2.setText(res[2])
        self.lineEdit_3.setText(res[3])
        self.lineEdit_4.setText(str(res[4])[:-2])
        self.lineEdit_5.setText(str(res[5]))
        
        #Удаление лишнего значения из Combobox
        if self.comboBox_4.itemText(self.comboBox_4.count()-1) == "":
            self.comboBox_4.removeItem(self.comboBox_4.count()-1)
            self.pushButton_8.setEnabled(False)
            self.pushButton_10.setEnabled(True)
        

    
    
    #Обработка окна Маршрут*******************************************************************
    def Route_settings(self):
        curs = self.conn.cursor()
        res = curs.execute('Select * from Route where ID_Shedule = 1').fetchall()
        curs.close()
        for number_station in res:
            self.comboBox_2.addItem(str(number_station[2]))
        try:
            self.lineEdit_6.setText(res[0][3])

            self.enable_settings([self.timeEdit_2, self.lineEdit_7], False)
            
            self.timeEdit.setTime(QTime.fromString(res[0][4][0:5], 'hh:mm'))
            self.timeEdit_2.setTime(QTime.fromString(res[0][5][0:5], 'hh:mm'))
            self.lineEdit_7.setText(str(res[0][6])[:-2])
        except: 
            self.lineEdit_6.setText('')
            self.timeEdit.setTime(QTime.fromString('00:00', 'hh:mm'))
            self.timeEdit_2.setTime(QTime.fromString('00:00', 'hh:mm'))
            self.lineEdit_7.setText('')
    
    def route_combobox_settings(self):  
        selected_index = self.comboBox.currentText()
        self.enable_settings([self.timeEdit_2, self.lineEdit_7], False)
        curs = self.conn.cursor()
        res = curs.execute('Select * from Route Where ID_Shedule = ?', (selected_index)).fetchall()
        
        if res != []:
            self.pushButton_8.setEnabled(False)
            self.pushButton_10.setEnabled(True)
            self.lineEdit_6.setText(res[0][3])
            self.timeEdit.setTime(QTime.fromString(res[0][4][0:5], 'hh:mm'))
            self.timeEdit_2.setTime(QTime.fromString(res[0][5][0:5], 'hh:mm'))
            self.lineEdit_7.setText(str(res[0][6])[:-2])
            
            self.comboBox_2.blockSignals(True)
            self.comboBox_2.clear()
    
            for number_station in res:
                self.comboBox_2.addItem(str(number_station[2]))
            self.comboBox_2.blockSignals(False)
        else:
            self.pushButton_8.setEnabled(True)
            self.pushButton_10.setEnabled(False)
            self.comboBox_2.blockSignals(True)
            self.comboBox_2.clear()
            self.comboBox_2.blockSignals(False)
            
            self.enable_settings([self.timeEdit_2, self.lineEdit_7], False)
            self.lineEdit_6.setText(curs.execute('Select firstStation FROM Schedule where ID = ?',(self.comboBox.currentText()) ).fetchone()[0])
            self.timeEdit.setTime(QTime.fromString('00:00', 'hh:mm'))
            self.timeEdit_2.setTime(QTime.fromString('00:00', 'hh:mm'))
            self.lineEdit_7.setText('')
        
        curs.close()
    
    def route_combobox_2_settings(self):
        selected_text_box = self.comboBox.currentText()
        selected_text_box2 = self.comboBox_2.currentText()
        if selected_text_box == '1':
            self.enable_settings([self.timeEdit_2, self.lineEdit_7], False)
        else:
            self.enable_settings([self.timeEdit_2, self.lineEdit_7], True)
            
        curs = self.conn.cursor()
        
        #Отключить кнопку если запись не была добавлена
        res = curs.execute('Select * from Route Where ID_Shedule = ? and NumberStation= ?', (selected_text_box, self.comboBox_2.itemText(self.comboBox_2.count()-1))).fetchone()
        if res == None:
            self.comboBox_2.removeItem(int(self.comboBox_2.count()-1))
            self.pushButton_8.setEnabled(False)
            self.pushButton_10.setEnabled(True)
            
        res = curs.execute('Select * from Route Where ID_Shedule = ? and NumberStation= ?', (selected_text_box, selected_text_box2)).fetchone()
        curs.close()

        self.lineEdit_6.setText(res[3])
        self.timeEdit.setTime(QTime.fromString(res[4][0:5], 'hh:mm'))
        self.timeEdit_2.setTime(QTime.fromString(res[5][0:5], 'hh:mm'))
        self.lineEdit_7.setText(str(res[6])[:-2])
    
    #Обработка окна Train*******************************************************************
    def train_settings(self):
        curs = self.conn.cursor()
        res = curs.execute('Select TimeArrival from Route Where ID_Shedule = 1 and NumberStation = 1').fetchone()[0]
        curs.close()
        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit_3.setTime(QTime.fromString(res[0:5], 'hh:mm'))
        self.enable_settings([self.timeEdit_3], False)
        
        #Настройка даты
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QDate.currentDate())
    
    def train_combobox_settings(self):
        selected_text_box = self.comboBox_3.currentText()
        curs = self.conn.cursor()
        try:
            res = curs.execute('Select TimeArrival from Route Where ID_Shedule = ? and NumberStation = 1',(selected_text_box)).fetchone()[0]
            curs.close()
            self.timeEdit_3.setTime(QTime.fromString(res[0:5], 'hh:mm'))
        except: 
            self.comboBox_3.setCurrentIndex(self.comboBox_3.currentIndex()-1)
            QtWidgets.QMessageBox.information(self, "Ошибка", 'Маршрут для данного расписания не построен!')
            
        
    #отключение виджетов   
    def enable_settings(self, widgets, status):
        for i in widgets:
            i.setEnabled(status)

    def block_buttons(self):
        tab_index = self.tabWidget.currentIndex()
        block_widgets = [self.pushButton_7, self.pushButton_8, self.pushButton_10]
        if tab_index == 0:
            if self.comboBox_4.itemText(self.comboBox_4.count()-1) == "":
                self.pushButton_8.setEnabled(True)
                self.pushButton_10.setEnabled(False)
            else:
                self.enable_settings([block_widgets[2], block_widgets[1]], False)
                self.enable_settings([block_widgets[0], block_widgets[2]], True)
        elif tab_index == 1:
            self.enable_settings([block_widgets[2], block_widgets[1]], False)
            self.enable_settings([block_widgets[0], block_widgets[2]], True)
        else:
            self.enable_settings([block_widgets[0], block_widgets[2]], False)
            self.enable_settings([block_widgets[2], block_widgets[1]], True)
            
    
    #Обработка Кнопок*******************************************************************
    
    def button_update(self):
        tab_index = self.tabWidget.currentIndex()
        
        if tab_index == 0:
            name_server_column = ['firstStation', 'lastStation', 'Weekdays', 'FullPrice', 'NumberStation']
            res_window = self.collect_widget_text([self.comboBox_4, self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5])
            res_window[4] = res_window[4]+'00'
            curs = self.conn.cursor()
            res_server = curs.execute('Select * from Schedule where ID = ?',(res_window[0])).fetchone()
            status = False
            for i in range(len(res_server)):
                
                if res_window[i] != str(res_server[i]):
                    status = True
                    curs.execute(f'UPDATE Schedule SET {name_server_column[i-1]} = ? where ID = ?', (res_window[i], res_window[0]))
                    curs.commit()
            
            if status:
                QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись была изменена!')
            else: QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись не была изменена!')
            
            curs.close()
        
        elif tab_index == 1:
            name_server_column = ['NameStation', 'TimeArrival', 'TimeParking', 'Price']
            res_window = self.collect_widget_text([self.comboBox, self.comboBox_2, self.lineEdit_6, self.timeEdit, self.timeEdit_2, self.lineEdit_7])
            
            curs = self.conn.cursor()
            res_server = curs.execute('Select * from Route where ID_Shedule = ? and Numberstation = ?', (res_window[0], res_window[1]) ).fetchone()
            status = False
            
            res_server = list(res_server)
            del res_server[0]
            del res_server[-1]
            res_window[5] = res_window[5]+'00'
            res_server[3] = res_server[3][:-3]
            res_server[4] = res_server[4][:-3]

            for i in range(len(res_server)):
                
                if str(res_window[i]) != str(res_server[i]):
                    status = True
                    curs.execute(f'UPDATE Route SET {name_server_column[i-2]} = ? where ID_Shedule = ? and Numberstation = ?', (res_window[i], res_window[0], res_window[1]) )
                    curs.commit()
            
            if status:
                QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись была изменена!')
            else: QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись не была изменена!')
            
            curs.close()
            
            
    def button_insert(self):
        tab_index = self.tabWidget.currentIndex()

        if tab_index == 0:
            res_window = self.collect_widget_text([self.comboBox_4, self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5])
 
            curs = self.conn.cursor()
            curs.execute('''INSERT INTO Schedule(firstStation, lastStation, Weekdays, FullPrice, NumberStation)
                                        VALUES(?,?,?,?,?)
                        ''', (res_window[1],res_window[2],res_window[3],res_window[4],res_window[5]))
            curs.commit()

            self.comboBox.addItem(str(curs.execute('select TOP 1 ID From Schedule  ORDER BY ID DESC').fetchone()[0]))
            item = str(curs.execute('select TOP 1 ID From Schedule  ORDER BY ID DESC').fetchone()[0])
            self.comboBox_4.setItemText(self.comboBox_2.count(), item)


            self.pushButton_8.setEnabled(False)
            self.pushButton_10.setEnabled(True)
            curs.close()
            QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись добавлена!')
            
        elif tab_index == 1:
            res_window = self.collect_widget_text([self.comboBox, self.comboBox_2, self.lineEdit_6, self.timeEdit, self.timeEdit_2, self.lineEdit_7])
 
            curs = self.conn.cursor()
            if res_window[1] == 1:
                res_window[-1] = 0

            curs.execute('''INSERT INTO Route(ID_Shedule, NumberStation, NameStation, TimeArrival, TimeParking, Price)
                                        VALUES(?,?,?,?,?,?)
                         ''', (int(res_window[0]), res_window[1],res_window[2], res_window[3], res_window[4], res_window[5])
                        )
            curs.commit()
            curs.close()

            self.pushButton_8.setEnabled(False)
            self.pushButton_10.setEnabled(True)
            QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись добавлена!')
            
        else: 
            res_window = self.collect_widget_text([self.comboBox_3, self.lineEdit_11, self.dateEdit, self.timeEdit_3, 
                                                   self.lineEdit_8, self.lineEdit_9,self.lineEdit_10])
            curs = self.conn.cursor()

            curs.execute('''INSERT INTO Train(ID_Shedule, Date, Time, NumberSV, NumberCoupe, NumberReserved, Code)
                                        VALUES(?,?,?,?,?,?,?)
                         ''',                (int(res_window[0]), res_window[2], res_window[3], 
                                              int(res_window[4]), int(res_window[5]), int(res_window[6]), res_window[1])
                        )
            try:
                curs.commit()
                QtWidgets.QMessageBox.information(self, "Сообщение", 'Запись добавлена!')
            except pyodbc.Error:
                QtWidgets.QMessageBox.information(self, "Ошибка зполнения", 'Поезд не ходит в этот день недели!')
            curs.close()
            
    
    def button_clear(self):
        tab_index = self.tabWidget.currentIndex()
        self.pushButton_8.setEnabled(True)
        if tab_index == 0:
            self.comboBox_4.blockSignals(True)
            self.comboBox_4.addItem("")
            self.comboBox_4.setCurrentIndex(self.comboBox_2.count())
            self.comboBox_4.blockSignals(False)
            
            self.pushButton_10.setEnabled(False)
            
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            
        elif tab_index == 1:
            self.pushButton_10.setEnabled(False)
            self.comboBox_2.blockSignals(True)
            self.comboBox_2.setCurrentIndex(self.comboBox_2.count()-1)
            self.comboBox_2.blockSignals(False)
            if self.comboBox_2.count() >= 1:
                self.enable_settings([self.timeEdit_2, self.lineEdit_7], True)
                self.comboBox_2.addItem(str(self.comboBox_2.count()+1))
                self.comboBox_2.blockSignals(True)
                self.comboBox_2.setCurrentIndex(self.comboBox_2.count()-1)
                self.comboBox_2.blockSignals(False)
            
            self.lineEdit_6.setText('')
            self.timeEdit.setTime(QTime.fromString('00:00', 'hh:mm'))
            self.timeEdit_2.setTime(QTime.fromString('00:00', 'hh:mm'))
            self.lineEdit_7.setText('')
            
        else:
            self.lineEdit_11.setText('')
            self.dateEdit.setDate(QDate.currentDate())
            self.lineEdit_8.setText('')
            self.lineEdit_9.setText('')
            self.lineEdit_10.setText('')
    
            
    
    #считывание данных с полей
    def collect_widget_text(self, widgets):
        text_list = []
        for widget in widgets:
            if isinstance(widget, QtWidgets.QLineEdit):
                text_list.append(widget.text())
            elif isinstance(widget, QtWidgets.QComboBox):
                text_list.append(widget.currentText())
            else:text_list.append(widget.text())
        return text_list