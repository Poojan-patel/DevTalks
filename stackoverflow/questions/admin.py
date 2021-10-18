from django.contrib import admin
from questions.models import Question, Tag, Answer

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
# Register your models here.
