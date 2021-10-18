from django.urls import path
from questions.views import read, readall

urlpatterns = [
     path('read/<uuid>/',read,name='read'),
     path('read/',readall,name='readall'),
]