from django.urls import path
from questions import views
from django.views.generic import TemplateView

urlpatterns = [
     path('read/<uuid>/',views.read,name='read'),
     path('read/',views.readall,name='readall'),
     path('editor/', TemplateView.as_view(template_name='editor.html'), name='question'),
     path('question/',views.add_question,name='add_question'),
     path('feed1/',views.get_feed,name='feed1'),
     path('editor_static/',TemplateView.as_view(template_name='editorStatic.html')),

     # Paths for EditorJS
     path('uploadImg/',views.upload_img, name='imageupload'),
     path('fileresp/<id>',views.fileresp),
     path('output/',views.output, name="output"),
]