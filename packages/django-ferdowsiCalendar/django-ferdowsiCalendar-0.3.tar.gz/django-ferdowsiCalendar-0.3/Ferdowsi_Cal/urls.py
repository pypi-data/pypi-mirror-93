from django.urls import path
from Ferdowsi_Cal.views import  getPersianMonth, getGregorianMonth,addEvent, addPersianEvent, editEvent, editPersianEvent, deleteEvent
app_name = 'Ferdowsi_Cal'
urlpatterns =[
    path('getGregorianMonth/<int:year>/<int:month>', getGregorianMonth),
    path('getPersianMonth/<int:year>/<int:month>', getPersianMonth),
    path('addEvent/<str:name>/<str:content>/<int:year>/<int:month>/<int:day>/<str:users>', addEvent),
    path('addPersianEvent/<str:name>/<str:content>/<int:year>/<int:month>/<int:day>/<str:users>', addPersianEvent),
    path('editeEvent/<str:name>/<str:content>/<int:year>/<int:month>/<int:day>/<int:id>/<str:users>', editEvent),
    path('editePersianEvent/<str:name>/<str:content>/<int:year>/<int:month>/<int:day>/<int:id>/<str:users>', editPersianEvent),
    path('deleteEvent/<int:id>', deleteEvent),
]