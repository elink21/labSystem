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
    query = f'select * from historiallendings where lendingDate> "{initialDate}" and lendingDate< "{endDate}" order by lendingDate'
    print(query)

    connection = startConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()

    filteredQuery = []

    # Not its time to do a little weird provisional join like operation
    for i in range(len(res)):
        accountNumber = res[i][3]
        patrimonialNumber = res[i][4]

        # Fetching extra information
        cursor.execute(
            f'select name from items where patrimonialNumber= {patrimonialNumber}')
        item = cursor.fetchall()

        res[i] = list(res[i])
        if len(item):
            res[i].append(item[0][0])
        else:
            res[i].append("GENERIC")

        cursor.execute(
            f'select name, career from students where accountNumber= {accountNumber}')
        student = cursor.fetchall()

        itemName = item[0][0] if len(item) else ""
        careerName = student[0][1] if len(student) else ""
        studentName = student[0][0] if len(student) else ""
        newLine = [res[i][1], res[i][2], studentName, itemName]

        if career == "all" or career == careerName:
            filteredQuery.append(newLine)

    for row in filteredQuery:
        print(row)

    connection.close()

    # Data filtering by career and info completion, first the data is filtered by the career
    return filteredQuery
