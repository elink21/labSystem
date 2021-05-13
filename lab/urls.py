
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('xlsStudents', views.xlsStudents, name='xlsStudents'),
    path('xlsLendings', views.xlsLendings, name='xlsLendings'),
    path('xlsItems', views.xlsItems, name='xlsItems'),
    path('createLending', views.createLending, name='createLending'),
    path('returnLending', views.returnLending, name='returnLending'),
    path('returnAllLendings', views.returnAllLendings, name='returnAllLendings'),
    path('importStudents', views.importStudents, name="importStudents"),
    path('importItems', views.importItems, name='importItems'),
    path('importLendings', views.importLendings, name='importLendings'),
    path('generateReport', views.generateReport, name="generateReport"),
]
