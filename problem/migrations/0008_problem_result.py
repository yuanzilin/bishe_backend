# Generated by Django 3.1.7 on 2021-03-30 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0007_problem_subtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='result',
            field=models.TextField(default=''),
        ),
    ]
