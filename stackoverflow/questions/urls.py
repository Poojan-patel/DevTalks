from django.urls import path
from questions import views

urlpatterns = [
     path('read/<uuid>/',views.read,name='read'),
     path('read/',views.readall,name='readall'),
     path('question/',views.add_question,name='add_question'),
     path('feed/',views.get_feed,name='feed')
]