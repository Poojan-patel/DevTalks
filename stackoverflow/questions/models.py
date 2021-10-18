from django.db import models
import uuid
# Create your models here


class Question(models.Model):
     id        = models.CharField(verbose_name='QuestionID',name='id',     primary_key=True, unique=True, editable=False, default=uuid.uuid4, max_length=40)
     user_id   = models.CharField(verbose_name='UserID',    name='user_id',blank=False,      null=False,  max_length=40)
     title     = models.CharField(verbose_name='Title',     name='title',  blank=False,      null=False,  max_length=100)
     body      = models.TextField(verbose_name='Body',      name='body',   blank=False,      null=False)


class Tag(models.Model):
     id        = models.AutoField(verbose_name='TagID',   name='id',  primary_key=True, editable=False)
     name      = models.CharField(verbose_name='TagName', name='tag', unique=True,      max_length=30, null=False, blank=False)

class Answer(models.Model):
     id        = models.CharField(verbose_name='AnswerID',    name='id',   primary_key=True,    default=uuid.uuid4,   unique=True,     editable=False, max_length=40)
     question  = models.ForeignKey(verbose_name='QuestionID', name='question' ,to=Question, null=False, blank=False,  related_name='answers', on_delete=models.CASCADE, to_field='id')
     body      = models.TextField(verbose_name='Body',        name='body', null=False, blank=False,)


# ForeignKey is same as DBMS, except a term, related_name="<NAME>"
# we can access one 2 many relationship from parent entity using related_name, defined in the foreignKey of child entity

# child_objects = parent_object.related_name.all()