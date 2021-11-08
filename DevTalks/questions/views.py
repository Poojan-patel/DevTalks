from django.http.response import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from questions.models import Question, Tag, Answer, Like, Upvote, Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,Count


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
     # print(data.user_id)
     # data.delete()
     # print(data.title)
     answers = data.answers.all()\
               .annotate(num_likes=Count('upvotes'))\
               .order_by('-num_likes')
     # print(answers)
     return render(request, 'questionRead.html', { 'question' : data, 'answers': answers })

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
          tags = request.POST['questionTag'].split(",")
          question = Question(user_id=user_id, title=title, body=body)
          question.save()
          
          for tag in tags:
               obj = Tag(question_id=question, tag=tag.strip())
               obj.save()

          messages.success(request,'Question added successfully')

     return redirect('feed')

@login_required(login_url='signin')
def edit_question(request, uuid):
     data = Question.objects.filter(id=uuid).first()
     if request.user.username != data.user.username:
          messages.error(request,'You are not Authorized to Edit the Question')
          return redirect('read', uuid=uuid)
     
     if request.method == "POST":
          data.title = request.POST['questionTitle']
          # if user_id data.user.id:
          data.body = request.POST['jsonData']
          tags = request.POST['questionTag'].split(",")
          Tag.objects.filter(question_id=data).delete()
          for tag in tags:
               obj = Tag(question_id=data, tag=tag.strip())
               obj.save()
          data.save()
          messages.success(request,'Question Updated successfully')
          return redirect('question_edit', uuid=uuid)
               
     return render(request, 'questionEdit.html', { 'question': data })


@login_required(login_url='signin')
def add_answer(request, question_id):
     if request.method == "POST":
          question = Question.objects.filter(id=question_id).first()
          myuser = request.user
          # print(myuser.username)
          body = request.POST['jsonData'].strip()
          print(body)

          answer = Answer(user=myuser, body=body, question_id=question)
          answer.save()
          messages.success(request, 'Answer added successfully')
          
          return redirect('read', uuid=question.id)

     return redirect('feed')

def get_feed(request):
     questions = Question.objects.all()
     # print(questions)
     tags = request.GET.get('tags',None)
     if tags is not None:
          tags = tags.split(',')
          for idx in range(len(tags)):
               tags[idx] = tags[idx].strip()
          #print(tags)
          #q = Q(tag='tag1') & Q(tag='tag2')
          #print(q)
          #Tag.objects.complex_filter()

          # 1. Fetch Questions based on the given tag list, 2. select only necessary fields
          # 3. add another field called annotate, which will group by based on the available fields in the QuerySet, here only Question
          # 4. Filter only those which are Exact match
          # 5. Select only question_id field
          # 6. Fetch the questions which were filtered based on the tags
          filtered_questions = Tag.objects.filter(tag__in=tags)\
                              .values('question_id')\
                              .annotate(cnt=Count('tag'))\
                              .filter(cnt=len(tags))\
                              .values('question_id')
          questions = Question.objects.filter(id__in=filtered_questions)
          #print(questions)
     
     
     # print(questions[0].tags)
     return render(request, 'feed.html', { 'questions' : questions })

@csrf_exempt
@login_required(login_url='signin')
def toggle_like(request,question_id):
     if request.method == "POST":
          # print(request.user.id)
          user = request.user
          like_status = Like.objects.filter(question_id=question_id, user=user).first()
          # print(like_status)
          try:
               if like_status is None:
                    add_like = Like(question_id_id=question_id, user=user)
                    add_like.save()
                    # return redirect('feed')
                    return JsonResponse({'Success':1})
               else:
                    like_status.delete()
                    # return redirect('feed')
                    return JsonResponse({'Success':2})
          except:
               # return redirect('feed')
               return JsonResponse({'Success':0})
          
@csrf_exempt
@login_required(login_url='signin')
def toggle_upvote(request,answer_id):
     # print(request.user.id)
     user = request.user
     upvote_status = Upvote.objects.filter(answer_id=answer_id, user=user).first()
     # print(upvote_status)
     try:
          if upvote_status is None:
               add_upvote = Upvote(answer_id=answer_id, user=user)
               add_upvote.save()
               return JsonResponse({'Success':1})
          else:
               upvote_status.delete()
               return JsonResponse({'Success':2})
     except:
          return JsonResponse({'Success':0})

@csrf_exempt
@login_required(login_url='signin')
def toggle_verify(request,answer_id):
     if request.method == "POST":
          # print(request.user.id)
          user = request.user
          answer = Answer.objects.filter(id=answer_id).first()
          if answer.question_id.user.username == user.username:
               answer.is_accepted = not answer.is_accepted
               answer.save()
               if answer.is_accepted:
                    return JsonResponse({'Success':1})
               else:
                    return JsonResponse({'Success':2})
                    
          return JsonResponse({'Success':0})