# Generated by Django 3.2.8 on 2021-10-18 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_delete_hello'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user_id',
            field=models.CharField(default='52cfc782-75aa-4222-a1d2-182ecdda84ee', max_length=40, verbose_name='UserID'),
            preserve_default=False,
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
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='questions.question', verbose_name='QuestionID')),
            ],
        ),
    ]
