from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from . import dbFunctions as db
from . import xlsFunctions as xls
from . import pdfFunctions as pdf
import json
import time
import pandas as pd
from datetime import datetime


# Create your views here.


def returnAllLendings(request):
    db.removeAllLendings()
    lendings = db.getLendings()
    historialLendings = db.getHistorialLendings()
    return HttpResponse(json.dumps({'lendings': lendings, 'historialLendings': historialLendings}),
                        content_type="application/json")


def returnLending(request):
    id = request.GET.get('id')

    db.removeByField('lendings', 'id', id)

    lendings = db.getLendings()
    historialLendings = db.getHistorialLendings()
    return HttpResponse(json.dumps({'lendings': lendings, 'historialLendings': historialLendings}),
                        content_type="application/json")


def createLending(request):
    accountNumber = request.GET.get('accountNumber')
    patrimonialNumber = request.GET.get('patrimonialNumber')

    db.insert('lendings',
              ['accountNumber', 'patrimonialNumber', 'lendingDate'],
              [accountNumber, patrimonialNumber, time.strftime('%Y-%m-%d %H:%M:%S')])

    lendings = db.getLendings()
    return HttpResponse(json.dumps(lendings), content_type="application/json")


def xlsLendings(request):
    output, name = xls.getList('historiallendings')

    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename={name}.xlsx'

    output.close()

    return response


def xlsItems(request):
    output, name = xls.getList('items')

    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={name}.xlsx"

    output.close()

    return response


def xlsStudents(request):
    output, name = xls.getList('students')

    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={name}.xlsx"

    output.close()

    return response


def index(request):
    students = db.getStudents()
    items = db.getItems()
    lendings = db.getLendings()
    historiallendings = db.getHistorialLendings()
    firstLending, lastLending = historiallendings[0], historiallendings[-1]

    careers = []
    for s in students:
        careers.append(s['career'])

    students = json.dumps(students)

    careerSet = list(set(careers))
    items = json.dumps(items)
    lendings = json.dumps(lendings)
    historiallendings = json.dumps(historiallendings)

    firstLending = int(firstLending["lendingDate"][0:4])
    lastLending = int(lastLending["lendingDate"][0:4])

    periodYears = []

    for i in range(firstLending, lastLending+1):
        periodYears.append(i)

    return render(request, 'base.html',
                  {'students': students, 'items': items,
                   'lendings': lendings, 'historialLendings': historiallendings,
                   'careers': careerSet,
                   'periodYears': periodYears})


def importStudents(request):
    studentsFile = request.FILES['studentsXLS']
    xl = pd.ExcelFile(studentsFile)
    df1 = xl.parse(xl.sheet_names[0])
    for index, row in df1.iterrows():
        student = {
            'name': row['name'],
            'accountNumber': row['accountNumber'],
            'career': row['career']
        }
        db.newStudent(student)
    return redirect('/')


def importItems(request):
    itemsFile = request.FILES['itemsXLS']
    xl = pd.ExcelFile(itemsFile)

    df1 = xl.parse(xl.sheet_names[0])
    for i, row in df1.iterrows():
        item = {
            'patrimonialNumber': row['patrimonialNumber'],
            'name': row['name'],
            'brand': row['brand'],
            'model': row['model'],
            'stock': row['stock']
        }
        db.newItem(item)
    return redirect('/')


def importLendings(request):
    lendingsFile = request.FILES['lendingsXLS']
    xl = pd.ExcelFile(lendingsFile)
    df1 = xl.parse(xl.sheet_names[0])
    for i, row in df1.iterrows():
        lending = {
            'lendingDate': row['lendingDate'],
            # change this line after db import
            'returnDate': row['lendingDate'],
            'accountNumber': row['accountNumber'],
            'patrimonialNumber': row['patrimonialNumber'],
        }
        print(lending)
        # Creating the lending
        db.insert('historialLendings',
                  ['accountNumber', 'patrimonialNumber',
                      'lendingDate', 'returnDate'],
                  [lending['accountNumber'], lending['patrimonialNumber'],
                      lending['lendingDate'], lending['returnDate']])
    return redirect('/')


def generateReport(request):
    initialDate = request.POST['initialDate']
    endDate = request.POST['endDate']
    career = request.POST['career']
    period = request.POST['period']
    periodYear = int(period[0:4])
    forPeriod = False

    print(period)

    # Turning dates into correct format
    if initialDate != "" and endDate != "":
        initialDate = datetime.strptime(initialDate, '%b %d, %Y')
        initialDate = initialDate.strftime('%Y-%m-%d')

        endDate = datetime.strptime(endDate, '%b %d, %Y')
        endDate = endDate.strftime('%Y-%m-%d')
    else:
        forPeriod = period
        if period[-1] == "A":
            initialDate = f'{periodYear}-02-01'
            endDate = f'{periodYear}-07-31'
        else:
            initialDate = f'{periodYear}-08-01'
            endDate = f'{periodYear+1}-01-31'

    dataForReport = db.queryForReport(initialDate, endDate, career)

    pdf.printFile(dataForReport, initialDate, endDate, career, forPeriod)
    # Now its time to return the file to the client
    fs = FileSystemStorage()
    filename = 'Reporte_de_uso.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf2:
            response = HttpResponse(pdf2, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Reporte de uso.pdf"'
            #response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
