# Generated by Django 3.2.6 on 2021-10-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='IsAccepted'),
        ),
    ]