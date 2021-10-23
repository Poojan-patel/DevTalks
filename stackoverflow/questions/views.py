from django.http.response import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from questions.models import Question, Answer, Like, Upvote, Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import io, time
from django.core.files.storage import default_storage


# Question Save Data Temp View
def output(request):
     if request.method == 'POST':
          # print(request.POST)
          question_title = request.POST['questionTitle']
          question_tag = request.POST['questionTag']
          json_data = request.POST['jsonData']
          # print(jsonData);
          return HttpResponse(question_title + "<br>" + question_tag + "<br>" + json_data)

def fileresp(request,id):
     img = Image.objects.get(id=id)
     obj = default_storage.open(str(img.image.name),'rb')
     # ip = io.StringIO()
     # ip.write("Hello")
     # op = io.BufferedReader(ip)
     # print(obj.read())
     return FileResponse(obj)

def read(request,uuid):
     data = Question.objects.filter(id=uuid).first()
     if data is None:
          return HttpResponse('None')
     print(data.user_id)
     data.delete()
     return HttpResponse(data)

@csrf_exempt
def upload_img(request):
     response_json = {
          'success': 0
     }
     if request.method == 'POST':
          #print("POST Method Called")
          name = request.FILES['image'].name
          request.FILES['image'].name = str(time.time())+ '.' +name.split('.')[-1]
          data = Image(image=request.FILES['image'])
          data.save()
          print(data.id)
          response_json['success'] = 1
          response_json['file'] = {
               'name': str(data.id),
               'url': '/question/fileresp/'+str(data.id)
          }
     else:
          print("Get Method Called")
     return JsonResponse(response_json)

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

@login_required(login_url='signin')
def add_question(request):
     if request.method == "GET":
          return redirect('signin')
     
     myuser = request.user
     user_id = myuser.id
     
     if user_id is not None:
          title = request.POST['questionTitle']
          body = request.POST['jsonData']
          question = Question(user_id=user_id, title=title, body=body)
          question.save()
          messages.success(request,'Question asked Successfully')

     return redirect('home')
     
@login_required(login_url='signin')
def add_answer(request, question_id):
     if request.method == "POST":
          myuser = request.user
          user_id = myuser.user_id
          body = request.POST['body'].strip()

          answer = Answer(user_id=user_id, body=body, question_id=question_id)
          answer.save()
          messages.success(request, 'Answer Conveyed Successfully')
          
          return redirect('home')

     return redirect('home')

def get_feed(request):
     questions = Question.objects.all()
     return render(request, 'feed.html', {'questions':questions})

@login_required(login_url='signin')
def toggle_like(request,question_id):
     myuser_id = request.user.user_id
     like_status = Like.objects.filter(question_id=question_id, user_id=myuser_id).first()
     if like_status is None:
          add_like = Like(user_id=myuser_id, question_id=question_id)
          add_like.save()
     else:
          like_status.delete()
     
     return redirect(request.get_full_path())

@login_required(login_url='signin')
def toggle_upvote(request,answer_id):
     myuser_id = request.user.user_id
     upvote_status = Upvote.objects.filter(answer_id=answer_id, user_id=myuser_id).first()
     if upvote_status is None:
          add_upvote = Upvote(user_id=myuser_id, answer_id=answer_id)
          add_upvote.save()
     else:
          upvote_status.delete()
     
     return redirect(request.get_full_path())
