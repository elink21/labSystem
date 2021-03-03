
from django.urls import path,include
from . import views
urlpatterns = [
    path('index',views.index,name='index'),
    path('xlsStudents',views.xlsStudents,name='xlsStudents'),
    path('xlsLendings',views.xlsLendings,name='xlsLendings'),
    path('xlsItems',views.xlsItems,name='xlsItems')

]
