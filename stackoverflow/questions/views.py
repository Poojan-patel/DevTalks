from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from questions.models import Question, Answer, Like, Upvote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def read(request,uuid):
     data = Question.objects.filter(id=uuid).first()
     if data is None:
          return HttpResponse('None')
     print(data.user_id)
     data.delete()
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

@login_required(login_url='signin')
def add_question(request):
     if request.method == "GET":
          return redirect('signin')
     
     myuser = request.user
     user_id = myuser.id
     title = request.POST['title'].strip()
     body = request.POST['body'].strip()

     if(title == "" or title is None):
          messages.error(request,'Title is Empty or It is not Valid')
          return redirect('add_question')
     
     if(body == "" or body is None):
          messages.error(request,'Body is Empty or It is not Valid')
          return redirect('add_question')
     
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

          if(body == "" or body is None):
               messages.error(request,"Answer can not be null")
               return redirect(request.request.get_full_path())
          
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
