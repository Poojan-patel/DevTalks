# Generated by Django 3.2.6 on 2021-10-23 08:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=40, primary_key=True, serialize=False, unique=True, verbose_name='AnswerID')),
                ('body', models.TextField(verbose_name='Body')),
                ('user_id', models.CharField(max_length=40, verbose_name='UserID')),
                ('is_accepted', models.BooleanField(verbose_name='IsAccepted')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=40, primary_key=True, serialize=False, unique=True, verbose_name='ImageID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=40, primary_key=True, serialize=False, unique=True, verbose_name='QuestionID')),
                ('user_id', models.CharField(max_length=40, verbose_name='UserID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
            ],
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=40, verbose_name='UserID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='questions.answer', verbose_name='AnswerID')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=40, verbose_name='UserID')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='questions.question', verbose_name='QuestionID')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questions.question', verbose_name='QuestionID'),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30, verbose_name='TagName')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question', verbose_name='QuestionID')),
            ],
            options={
                'unique_together': {('question_id', 'tag')},
            },
        ),
    ]