from django.urls import path
from questions import views
from django.views.generic import TemplateView

urlpatterns = [
     path('read/<uuid>/',views.read,name='read'),
     path('read/',views.readall,name='readall'),
     path('create/', TemplateView.as_view(template_name='questionCreate.html'), name='question_read'),
     path('edit/<uuid>/', views.edit_question, name='question_edit'),
     path('question/',views.add_question,name='add_question'),
     path('answer/<question_id>/',views.add_answer,name='add_answer'),
     path('feed1/',views.get_feed,name='feed1'),
     path('question-read/',TemplateView.as_view(template_name='questionRead.html')),

     # Paths for EditorJS
     path('uploadImg/',views.upload_img, name='imageupload'),
     path('fileresp/<id>',views.fileresp),
     path('output/',views.output, name="output"),
]