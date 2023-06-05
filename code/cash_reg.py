from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, Qt
import rout_train, Save_pdf, Dialog_rout_train

from Frame import cash_register

class cash_regApp(QtWidgets.QMainWindow, cash_register.Ui_MainWindow):
    def __init__(self,parent, conn):
        super().__init__(parent)
        self.setupUi(self)
        self.conn = conn
        self.dateEdit.setDate(QDate.currentDate())
        self.pushButton.clicked.connect(self.finde)
        self.action.triggered.connect(self.ShowDialog) #Меню(выходной документ)
        self.dateEditSettings()

    def dateEditSettings(self):
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QDate.currentDate())
    
    def finde(self):
        start = self.lineEdit.text()
        end = self.lineEdit_2.text()
        date = self.dateEdit.date()
        self.finde_route(start, end, date.toString('dd-MM-yyyy'))
        
    def finde_route(self, start_st, end_st, date_st):

        start_st ='Медногорск' 
        end_st='Самара'
        date_st='17-05-2023'
        query = f"""
                Select DIstinct Train.Code, '{start_st}' as startt, '{end_st}' as endd,
                    '{date_st}' as start_Date,
                    (Select IIF(Route.TimeParking = '00:00', Route.TimeArrival, 
                                        DATEADD(HH, CONVERT(INTEGER,FORMAT(route.TimeParking,'hh')), DATEADD(MI, CONVERT(INTEGER,FORMAT(route.TimeParking,'mm')), Route.TimeArrival))
                                        )
                            from Route 
                            Where Route.NameStation = '{start_st}' and Route.ID_Shedule = Schedule.ID) as time_start,

                     FORMAT(DateAdd(HOUR, (Select SUM(Route.h_from_station) From Route WHERE Route.ID_Shedule = Schedule.ID 
																					  AND   Route.NumberStation <= (SELECT Route.NumberStation FROM Route 
																													Where Route.ID_Shedule = Schedule.ID
																													AND   Route.NameStation = '{end_st}')),
                           DATEADD(HH,  CONVERT(INTEGER, FORMAT(Train.Time, 'hh')), CONVERT(DATETIME, Train.Date))), 'dd.MM.yyyy') as DateArrival,

                    (Select Route.TimeArrival from Route 
                                Where Route.NameStation = '{end_st}' and Route.ID_Shedule = Schedule.ID) as TimeEnd,
                                
                    (Select Sum(Price)*0.7 From (Select Distinct Route.ID, Route.NameStation, Route.Price  From Route
                        Join Schedule ON Schedule.ID = Route.ID_Shedule
                        Join Train as tr ON tr.ID_Shedule = Schedule.ID        
                    Where Train.Code = tr.Code
                            AND Route.ID > (Select ID From Route R Where NameStation = '{start_st}' and R.ID_Shedule = Schedule.ID )
                            AND Route.ID <= (Select ID From Route R1 Where NameStation = '{end_st}' and R1.ID_Shedule = Schedule.ID)) as P) as Plac,
                    
                    (Select Sum(Price) From (Select Distinct Route.ID, Route.NameStation, Route.Price  From Route
                        Join Schedule ON Schedule.ID = Route.ID_Shedule
                        Join Train as tr ON tr.ID_Shedule = Schedule.ID        
                    Where Train.Code = tr.Code
                            AND Route.ID > (Select ID From Route R Where NameStation = '{start_st}' and R.ID_Shedule = Schedule.ID )
                            AND Route.ID <= (Select ID From Route R1 Where NameStation = '{end_st}' and R1.ID_Shedule = Schedule.ID)) as P) as Coupe,
    
                    (Select Sum(Price)*1.5 From (Select Distinct Route.ID, Route.NameStation, Route.Price  From Route
                        Join Schedule ON Schedule.ID = Route.ID_Shedule
                        Join Train as tr ON tr.ID_Shedule = Schedule.ID        
                    Where Train.Code = tr.Code
                            AND Route.ID > (Select ID From Route R Where NameStation = '{start_st}' and R.ID_Shedule = Schedule.ID )
                            AND Route.ID <= (Select ID From Route R1 Where NameStation = '{end_st}' and R1.ID_Shedule = Schedule.ID)) as P) as SV,
                    
                    Train.ID

                From Train
                    JOIN Schedule ON Schedule.ID = Train.ID_Shedule
                    JOIN Route ON Route.ID_Shedule = Schedule.ID
                Where
                    (FORMAT(DateAdd(HOUR, 
                                    (Select SUM(Route.h_from_station) From Route 
                                        WHERE Route.ID <= (Select Route.ID FROM Route WHERE Route.NameStation = '{start_st}' AND Route.ID_Shedule = Schedule.ID)
                                        AND Route.ID_Shedule = Schedule.ID),
                                    DATEADD(HH,  CONVERT(INTEGER, FORMAT(Train.Time, 'hh')), CONVERT(DATETIME, Train.Date))
                                    ), 'dd.M.yyyy')) = CONVERT(DATE, '{date_st}', 104)
            """
        
        curs = self.conn.cursor()
        curs.execute(query)
        res = curs.fetchall()
        curs.close()
        
        if res == []:
            QtWidgets.QMessageBox.information(self, "Результат поиска", 'По этому маршруту поезда не найдены!')
        else:
            #Переход к другому окну
            self.hide()
            self.route_train_Window = rout_train.route_trainApp(self, res, self.conn)
            self.route_train_Window.LoadTrain()
            self.route_train_Window.show()

    def route_train(self, curDate):
        curs = self.conn.cursor()
        query = '''
                SELECT Train.Code, R1.NameStation, 
                    FORMAT(DateAdd(HOUR, (Select SUM(Route.h_from_station) From Route WHERE Route.ID_Shedule = Schedule.ID
                                                                                        AND Route.NumberStation <= R1.NumberStation),
                    DATEADD(HH,  CONVERT(INTEGER, FORMAT(Train.Time, 'hh')), CONVERT(DATETIME, Train.Date))), 'dd.MM.yyyy') AS startDate,

                    R1.TimeArrival, R1.TimeParking,
                    
                    DATEADD(HH, CONVERT(INTEGER ,FORMAT(R1.TimeParking,'hh')), DATEADD(MI, CONVERT(INTEGER,FORMAT(R1.TimeParking,'mm')), 
                                    R1.TimeArrival)) AS StartTime

                FROM Train
                INNER JOIN Schedule ON Schedule.ID = Train.ID_Shedule
                INNER JOIN Route as R1 ON R1.ID_Shedule = Schedule.ID

                Where Train.Date = ?
                '''
        res = curs.execute(query, (curDate)).fetchall()
        curs.close()
        Save_pdf.train_route(res)


    def ShowDialog(self):
        dialog = Dialog_rout_train.rout_train_window(self)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            selected_date = dialog.findChild(QtWidgets.QDateEdit).date()
            #curDate = '17.05.2023'
            #self.route_train(curDate)
            self.route_train(selected_date.toString(Qt.ISODate))
