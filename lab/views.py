from django.shortcuts import render
from django.http.response import HttpResponse
from . import dbFunctions as db
from . import xlsFunctions as xls
import json

# Create your views here.


def xlsLendings(request):
    output,name = xls.getList('historiallendings')

    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename={name}.xlsx'

    output.close()

    return response


def xlsItems(request):
    output,name = xls.getList('items')

    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={name}.xlsx"

    output.close()

    return response


def xlsStudents(request):
    output,name= xls.getList('students')

    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={name}.xlsx"

    output.close()

    return response


def index(request):
    students = db.getStudents()
    items = db.getItems()
    lendings = db.getLendings()

    students = json.dumps(students)
    items = json.dumps(items)
    lendings = json.dumps(lendings)

    return render(request, 'base.html', {'students': students, 'items': items, 'lendings': lendings})
