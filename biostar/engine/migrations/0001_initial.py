# Generated by Django 2.0.1 on 2018-02-21 18:26

import biostar.engine.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.IntegerField(choices=[(1, 'No Access'), (2, 'Read Access'), (3, 'Write Access'), (4, 'Owner Access')], default=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('security', models.IntegerField(choices=[(1, 'Authorized'), (2, 'Authorization Required')], default=2)),
                ('deleted', models.BooleanField(default=False)),
                ('uid', models.CharField(max_length=32, unique=True)),
                ('sticky', models.BooleanField(default=False)),
                ('name', models.CharField(default='No name', max_length=256)),
                ('summary', models.TextField(default='No summary.')),
                ('text', models.TextField(default='No description.', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('json_text', models.TextField(default='{}', max_length=10000)),
                ('template', models.TextField(default='')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default=None, help_text='Optional image', max_length=1024, upload_to=biostar.engine.models.image_path)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(1, 'Pending'), (2, 'Ready'), (3, 'Error')], default=1)),
                ('method', models.IntegerField(choices=[(1, 'Linked Data'), (2, 'Uploaded Data')], default=1)),
                ('name', models.CharField(default='name', max_length=256)),
                ('summary', models.TextField(blank=True, default='summary', max_length=10000)),
                ('image', models.ImageField(blank=True, default=None, max_length=1024, upload_to=biostar.engine.models.image_path)),
                ('sticky', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, default='description', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(default='DATA', max_length=256)),
                ('size', models.IntegerField(default=0)),
                ('file', models.FilePathField(max_length=1024)),
                ('uid', models.CharField(max_length=32, unique=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(1, 'Queued'), (2, 'Running'), (6, 'Paused'), (5, 'Spooled'), (3, 'Completed'), (4, 'Error')], default=1)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(default='name', max_length=256)),
                ('summary', models.TextField(default='summary')),
                ('image', models.ImageField(blank=True, default=None, max_length=1024, upload_to=biostar.engine.models.image_path)),
                ('text', models.TextField(default='description', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('sticky', models.BooleanField(default=False)),
                ('json_text', models.TextField(default='commands')),
                ('uid', models.CharField(max_length=32)),
                ('template', models.TextField(default='makefile')),
                ('security', models.IntegerField(choices=[(1, 'Authorized'), (2, 'Authorization Required')], default=2)),
                ('script', models.TextField(default='')),
                ('stdout_log', models.TextField(default='', max_length=200000)),
                ('stderr_log', models.TextField(default='', max_length=200000)),
                ('valid', models.BooleanField(default=True)),
                ('path', models.FilePathField(default='')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Analysis')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sticky', models.BooleanField(default=False)),
                ('privacy', models.IntegerField(choices=[(3, 'Private'), (2, 'Shareable Link'), (1, 'Public')], default=3)),
                ('image', models.ImageField(blank=True, default=None, max_length=1024, upload_to=biostar.engine.models.image_path)),
                ('name', models.CharField(default='name', max_length=256)),
                ('summary', models.TextField(default='summary', max_length=10000)),
                ('deleted', models.BooleanField(default=False)),
                ('text', models.TextField(default='description', max_length=10000)),
                ('html', models.TextField(default='html', max_length=200000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('uid', models.CharField(max_length=32, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
        migrations.AddField(
            model_name='data',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
        migrations.AddField(
            model_name='access',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
        migrations.AddField(
            model_name='access',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
