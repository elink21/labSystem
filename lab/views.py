from django.shortcuts import render
from . import dbFunctions as db
import json

# Create your views here.


def index(request):
    students = db.getStudents()
    items = db.getItems()
    lendings = db.getLendings()

    students = json.dumps(students)
    items = json.dumps(items)
    lendings = json.dumps(lendings)

    return render(request, 'base.html', {'students': students, 'items': items, 'lendings': lendings})
