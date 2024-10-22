# Generated by Django 3.2.9 on 2021-11-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopicRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('keyword', models.CharField(max_length=100)),
                ('confidence', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'meaningful_topics',
                'managed': False,
            },
        ),
    ]
