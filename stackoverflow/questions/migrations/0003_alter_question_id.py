# Generated by Django 3.2.8 on 2021-10-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_alter_question_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='QuestionID'),
        ),
    ]