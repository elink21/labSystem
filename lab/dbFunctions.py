from mysql.connector import connect, Error


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

    #fields are id, lendingDate, accountNumber and patrimonialNumber

    for lending in lendings:
        newLending={}
        newLending['id'] = lending[0]
        newLending['lendingDate'] = lending[1]
        newLending['accountNumber'] = lending[2]
        newLending['patrimonialNumber'] = lending[3]

        lendingsDicts.append(newLending)

    return lendingsDicts

print(getLendings())
