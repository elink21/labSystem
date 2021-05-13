from mysql.connector import connect
import datetime
import time


def getQuery(cursor, table: str) -> list:
    cursor.execute(f'select * from {table}')
    res = cursor.fetchall()
    return res


def startConnection():
    c = connect(
        host="localhost",
        user="root",
        password="*v%_M_%m9S$4Y5+%",
        database='culab'
    )
    return c


def removeAllLendings():
    connection = startConnection()
    cursor = connection.cursor()

    cursor.execute(f'select * from lendings')

    activeLendings = cursor.fetchall()

    for lending in activeLendings:
        removeByField('lendings', 'id', lending[0])


def removeByField(table: str, field: str, value):

    connection = startConnection()
    cursor = connection.cursor()

    # Copying from actualLending to the historial
    cursor.execute(f'select * from lendings where {field} = {value}')
    res = cursor.fetchall()[0]
    print(res)
    returnDate = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
    statement = f"insert into historiallendings(returnDate,lendingDate,accountNumber,patrimonialNumber) values('{returnDate}','{res[1]}',{res[2]},{res[3]})"
    print(statement)
    print("*"*10)
    cursor.execute(statement)

    statement = f'delete from {table} where {field} = {value}'
    cursor.execute(statement)
    connection.commit()
    connection.close()
    return True


def getList(table: str) -> list:
    connection = startConnection()
    l = getQuery(connection.cursor(), table)
    return list(l)


def getStudents() -> list:
    connection = startConnection()
    students = getQuery(connection.cursor(), "students")
    connection.close()

    # Fields are id, name, account, career
    studentsDicts = []
    for student in students:
        newStudent = {}
        newStudent['id'] = student[0]
        newStudent['name'] = student[1]
        newStudent['accountNumber'] = student[2]
        newStudent['career'] = student[3]
        studentsDicts.append(newStudent)

    return studentsDicts


def getItems() -> list:
    connection = startConnection()
    items = getQuery(connection.cursor(), "items")
    connection.close()

    itemsDicts = []

    for item in items:

        newItem = {}

        # fields are id, patrimonialNumber, name, brand, model and stock
        newItem['id'] = item[0]
        newItem['patrimonialNumber'] = item[1]
        newItem['name'] = item[2]
        newItem['brand'] = item[3]
        newItem['model'] = item[4]
        newItem['stock'] = item[5]

        itemsDicts.append(newItem)

    return itemsDicts


def getLendings() -> list:
    connection = startConnection()
    lendings = getQuery(connection.cursor(), "lendings")
    connection.close()

    lendingsDicts = []

    # fields are id, lendingDate, accountNumber and patrimonialNumber

    for lending in lendings:
        newLending = {}
        newLending['id'] = lending[0]
        newLending['lendingDate'] = str(lending[1])
        newLending['accountNumber'] = lending[2]
        newLending['patrimonialNumber'] = lending[3]

        lendingsDicts.append(newLending)

    return lendingsDicts


def getHistorialLendings() -> list:
    connection = startConnection()
    lendings = getQuery(connection.cursor(), "historiallendings")
    connection.close()

    lendingsDicts = []

    # fields are id, lendingDate, accountNumber and patrimonialNumber

    for lending in lendings:
        newLending = {}
        newLending['id'] = lending[0]
        newLending['returnDate'] = str(lending[2])
        newLending['lendingDate'] = str(lending[1])
        newLending['accountNumber'] = lending[3]
        newLending['patrimonialNumber'] = lending[4]

        lendingsDicts.append(newLending)

    return lendingsDicts


def insert(table: str, fields: list, values: list) -> bool:
    # Generating sql query from params
    statement = f'Insert into {table} ('
    for i in range(len(fields)):
        statement += fields[i]
        if i != len(fields)-1:
            statement += ','
    statement += ') values ('

    for i in range(len(values)):
        statement += "%s"
        if i != len(fields)-1:
            statement += ','
    statement += ')'

    print(statement)
    connection = startConnection()
    cursor = connection.cursor()
    cursor.execute(statement, values)
    connection.commit()
    connection.close()
    return True


def newStudent(student):
    allStudents = getStudents()
    # Checking for duplicates
    for x in allStudents:
        if(x['accountNumber'] == student['accountNumber']):
            return
    insert('students', ['name', 'accountNumber', 'career'],
           [student['name'], student['accountNumber'], student['career']])


def newItem(item):
    allItems = getItems()
    # Duplicates
    for x in allItems:
        if(x['patrimonialNumber'] == str(item['patrimonialNumber'])):
            return
    insert('items', ['patrimonialNumber', 'name', 'brand', 'model', 'stock'],
           [item['patrimonialNumber'], item['name'], item['brand'], item['model'], item['stock']])


def queryForReport(initialDate, endDate, career):
    query = ""
    if(career != 'all'):
        query = f'select lendingDate,returnDate,students.name,items.name from historiallendings join students on students.accountNumber join items on historiallendings.patrimonialNumber where lendingDate>"{initialDate}" and lendingDate<"{endDate}" and students.career="{career}" ORDER BY lendingDate'
    else:
        query = f'select lendingDate,returnDate,students.name,items.name from historiallendings join students on students.accountNumber join items on historiallendings.patrimonialNumber where lendingDate>"{initialDate}" and lendingDate<"{endDate}" ORDER BY lendingDate'

    connection = startConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    for row in res:
        print(row[0])
    return res
