# Generated by Django 3.2.8 on 2021-11-03 05:08

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_results', '0010_remove_duplicate_indices'),
        ('labeling', '__first__'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('mode', models.CharField(blank=True, choices=[('NER', 'Ner'), ('TEXTCAT', 'Textcat'), ('textcat_multilabel', 'Textcat Multilabel')], default='NER', max_length=50, null=True)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Model Tags')),
            ],
            options={
                'db_table': 'models',
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('input_meta', models.JSONField(blank=True, default=dict)),
                ('train_meta', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='labeling.dataset')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.model')),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_results.taskresult')),
            ],
            options={
                'db_table': 'trains',
            },
        ),
    ]
