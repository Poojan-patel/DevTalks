from django.db import models
from users.models import User
import uuid
# Create your models here


class Question(models.Model):
     id        = models.CharField(verbose_name='QuestionID',name='id',      primary_key=True, unique=True, editable=False, default=uuid.uuid4, max_length=40)
     user      = models.ForeignKey(User, on_delete=models.CASCADE,          blank=True, null=True)
     title     = models.CharField(verbose_name='Title',     name='title',   blank=False, null=False, max_length=100)
     body      = models.TextField(verbose_name='Body',      name='body',    blank=False, null=False)

class Tag(models.Model):
     question_id    = models.ForeignKey(verbose_name='QuestionID',  name='question_id', to=Question, on_delete=models.CASCADE, blank=False, null=False)
     tag           = models.CharField(verbose_name='TagName',       name='tag', max_length=30, blank=False, null=False)

     class Meta:
          unique_together = (('question_id', 'tag'),)

class Answer(models.Model):
     id          = models.CharField(verbose_name='AnswerID',      name='id',          primary_key=True,    default=uuid.uuid4,   unique=True,     editable=False, max_length=40)
     question    = models.ForeignKey(verbose_name='QuestionID',   name='question_id',   to=Question, null=False, blank=False,  related_name='answers', on_delete=models.CASCADE, to_field='id')
     body        = models.TextField(verbose_name='Body',          name='body',        blank=False, null=False)
     user        = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
     is_accepted = models.BooleanField(verbose_name='IsAccepted', name='is_accepted', default=False, blank=False, null=False)

class Like(models.Model):
     user     = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
     question = models.ForeignKey(verbose_name='QuestionID', name='question_id' ,to=Question,   null=False,  blank=False,  related_name='likes', on_delete=models.CASCADE, to_field='id')

class Upvote(models.Model):
     user   = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
     answer = models.ForeignKey(verbose_name='AnswerID', name='answer',  to=Answer, to_field='id', null=False, blank=False, related_name='upvotes', on_delete=models.CASCADE)

class Image(models.Model):
     id = models.CharField(verbose_name='ImageID', name='id',    primary_key=True,    default=uuid.uuid4,   unique=True,     editable=False, max_length=40)
     img = models.ImageField(verbose_name='Image', name='image', upload_to='images/')


# ForeignKey is same as DBMS, except a term, related_name="<NAME>"
# we can access one 2 many relationship from parent entity using related_name, defined in the foreignKey of child entity

# child_objects = parent_object.related_name.all()