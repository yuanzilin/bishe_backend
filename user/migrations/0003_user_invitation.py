# Generated by Django 3.1.7 on 2021-03-11 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210311_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='invitation',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]