# Generated by Django 3.2.8 on 2021-12-10 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_prediction_commit_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='ignore_committed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
