# Generated by Django 2.1.5 on 2019-01-25 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_project_actve'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='nme',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]