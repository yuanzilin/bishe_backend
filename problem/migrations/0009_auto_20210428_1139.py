# Generated by Django 3.1.7 on 2021-04-28 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_problem_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='celery_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='problem',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_limit',
            field=models.IntegerField(default=10),
        ),
    ]