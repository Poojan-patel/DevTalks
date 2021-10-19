from django.contrib import admin
from questions.models import Like, Upvote, Question, Tag, Answer

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register([Like, Upvote])
# Register your models here.
