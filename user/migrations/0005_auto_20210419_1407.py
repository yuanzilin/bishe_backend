# Generated by Django 3.1.7 on 2021-04-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_tasknumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='serviceNumber',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='toolNumber',
            field=models.IntegerField(default=0),
        ),
    ]