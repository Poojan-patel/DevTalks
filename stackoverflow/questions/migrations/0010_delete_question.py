# Generated by Django 3.2.8 on 2021-10-18 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_alter_question_user_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Question',
        ),
    ]