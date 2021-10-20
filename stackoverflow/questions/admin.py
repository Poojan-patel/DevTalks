from django.contrib import admin
from questions.models import Like, Upvote, Question, Tag, Answer, Image

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register([Like, Upvote, Image])
# Register your models here.
