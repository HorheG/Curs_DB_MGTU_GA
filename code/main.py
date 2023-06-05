import sys
import cash_reg, operator_wind
import Connect_db
from Frame import authorization

from PyQt5 import QtWidgets



class authorizationApp(QtWidgets.QMainWindow, authorization.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = None
        self.pushButton.clicked.connect(self.connect_db)
        self.pushButton_2.clicked.connect(sys.exit)
        
        
    def login(self):
        self.cash_register_Window = cash_reg.cash_regApp(self, self.conn)
        self.hide()
        self.cash_register_Window.show()
    
    def login_oper(self):
        self.oper_window = operator_wind.operator_app(self.conn)
        self.hide()
        self.oper_window.show()
        
    
    def connect_db(self):
        server = 'DESKTOP-PSTB5KT'  # Имя сервера MS SQL Server
        database = 'RJD'  # Имя базы данных
        username = self.lineEdit.text()  # Имя пользователя
        password = self.lineEdit_2.text()  # Пароль пользователя
        if username == '' or password == '':
             QtWidgets.QMessageBox.information(self, "Авторизация", 'Логин или пароль введены неверно!')
        else:
            try:
                self.conn = Connect_db.connet_user(server, database, username, password)
                query = f"SELECT r.name AS RoleName FROM sys.syslogins l JOIN sys.sysusers u ON l.sid = u.sid JOIN sys.database_role_members m ON u.uid = m.member_principal_id JOIN sys.database_principals r ON m.role_principal_id = r.principal_id WHERE l.name = '{username}'"
                cursor = self.conn.cursor()
                role = cursor.execute(query).fetchone()[0]
                if role == "Cashier": self.login()
                elif role == "Operator": self.login_oper()
                cursor.close()
            except Connect_db.pyodbc.InterfaceError:
                QtWidgets.QMessageBox.information(self, "Авторизация", 'Логин или пароль введены неверно!')

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = authorizationApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()