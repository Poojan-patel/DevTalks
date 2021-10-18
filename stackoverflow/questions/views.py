from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from questions.models import Question, Answer

# Create your views here.

def read(request,uuid):
     data = Question.objects.filter(id=uuid).first()
     print(data.user_id)
     return HttpResponse(data)

def readall(request):
     data = Question.objects.all()
     st = "<ol>"
     for d in data:
          t = '<li>' + str(d.id) + '<ul>'
          for a in d.answers.all():
               t = t + '<li>' + str(a.id) + '</li>'
          # print(d.answers.all())
          st = st + t + '</ul></li>'
     
     return HttpResponse(st+'</ol>')