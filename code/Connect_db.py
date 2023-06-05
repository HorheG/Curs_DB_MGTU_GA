import pyodbc    
def connet_user(server, database, username, password):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    connection = pyodbc.connect(connection_string)
    return connection
    '''
    query = f"SELECT r.name AS RoleName FROM sys.syslogins l JOIN sys.sysusers u ON l.sid = u.sid JOIN sys.database_role_members m ON u.uid = m.member_principal_id JOIN sys.database_principals r ON m.role_principal_id = r.principal_id WHERE l.name = '{username}'"

    cursor.execute(query)

    # Получение результатов
    roles = [row.RoleName for row in cursor.fetchall()]

    # Вывод ролей
    for role in roles:
        print(role)
    '''
    

'''
server = 'DESKTOP-PSTB5KT'  # Имя сервера MS SQL Server
database = 'RJD'  # Имя базы данных
username = 'Игумнова'  # Имя пользователя
password = '1111'  # Пароль пользователя

conn = connet_user(server, database, username, password)
cursor = conn.cursor()
f = 'У128'
cursor.execute('Update Train Set Code = ? where ID = 35',(f))
cursor.commit()
cursor.close()
'''
#query = f"SELECT r.name AS RoleName FROM sys.syslogins l JOIN sys.sysusers u ON l.sid = u.sid JOIN sys.database_role_members m ON u.uid = m.member_principal_id JOIN sys.database_principals r ON m.role_principal_id = r.principal_id WHERE l.name = '{username}'"
#cursor.execute(query)

    
