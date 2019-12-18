import pyodbc
# .\KONRADKSQL
# Chmury



def TryConnection(user,password):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.\KONRADKSQL;'
                              'Database=Chmury;'
                              'UID=' + user + ';'
                              'PWD=' + password + ';'
                              'Trusted_connectrion=False')
        return True
    except:
        return False
    finally:
        None


def ExecuteQuery(QueryCommand, user, password):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.\KONRADKSQL;'
                              'Database=Chmury;'
                              'UID='+user+';'
                              'PWD='+password+';')
        cursor = conn.cursor()
        cursor.execute(QueryCommand)
        return cursor
    except:
        print(QueryCommand + " error")
        return False
    finally:
        None


def InsertData(InsertCommand, user, password):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.\KONRADKSQL;'
                              'Database=Chmury;'
                              'UID=' + user + ';'
                              'PWD=' + password + ';')
        cursor = conn.cursor()
        cursor.execute(InsertCommand)
        conn.commit()
        return True
    except:
        print(InsertCommand + " error")
        return False


def InsertImage(imagepath, name, user, password):
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=.\KONRADKSQL;'
                              'Database=Chmury;'
                              'UID=' + user + ';'
                              'PWD=' + password + ';')
        cursor = conn.cursor()
        with open(imagepath, 'rb') as photo_file:
            photo_bytes = photo_file.read()
        cursor.execute("INSERT INTO pictures (img) VALUES (?)", photo_bytes)
        conn.commit()
        cursor = conn.cursor()
        x = cursor.execute("SELECT TOP 1 id from pictures order by id desc").fetchall()
        cursor = conn.cursor()
        cursor.execute("update pictures set [user] = '"+user+"', timestamp = CURRENT_TIMESTAMP, name = '"+name+"' WHERE id = "+str(x[0][0]))
        conn.commit()
        return True
    except Exception as e:
        print("Insert image error")
        print(str(e))
        return False


def InsertCloud(imagepath,imagename, user, password):
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=.\KONRADKSQL;'
                              'Database=Chmury;'
                              'UID=' + user + ';'
                              'PWD=' + password + ';')
        cursor = conn.cursor()
        with open(imagepath, 'rb') as photo_file:
            photo_bytes = photo_file.read()
        cursor.execute("INSERT INTO clouds (img) VALUES (?)", photo_bytes)
        conn.commit()
        cursor = conn.cursor()
        x = cursor.execute("SELECT TOP 1 id from clouds order by id desc").fetchall()[0][0]
        cursor = conn.cursor()
        cursor.execute("update clouds set machine = 'y',approved = 'n', name = '"+imagename+"' where id = "+str(x))
        conn.commit()
        return True
    except Exception as e:
        print("Insert cloud error")
        print(str(e))
        return False
