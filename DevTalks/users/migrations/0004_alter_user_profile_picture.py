# Generated by Django 3.2.6 on 2021-10-24 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_phone_user_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profile_pics/default.svg', upload_to='profile_pics'),
        ),
    ]
