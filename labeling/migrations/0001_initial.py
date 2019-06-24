# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2019-04-20 20:20
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_examples', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('complete_indicator', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('expiry_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='HIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_examples', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('assignment_num', models.IntegerField()),
                ('assignment_complete_num', models.IntegerField()),
                ('assignment_id_list', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('user_id_list', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('expiry_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('worker_id_set', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('descriptions', models.TextField(blank=True, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('HIT_capacity', models.IntegerField(default=5)),
                ('label_policy', models.IntegerField(default=1)),
                ('assignment_total', models.IntegerField(default=2)),
                ('age', models.IntegerField(choices=[(0, 'not sure'), (1, 'under 10'), (2, '11 to 20'), (3, '21 to 30'), (4, '31 to 40'), (5, 'above 41')], default=0)),
                ('gender', models.IntegerField(choices=[(0, 'not sure'), (1, 'female'), (2, 'male')], default=0)),
                ('career', models.IntegerField(default=0)),
                ('location', models.IntegerField(default=0)),
                ('approval_rate', models.DecimalField(decimal_places=4, default=0, max_digits=5)),
                ('approval_HIT_number', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expiry_time', models.DateTimeField()),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to='data/')),
                ('complete_indicator', models.BooleanField(default=False)),
                ('table_complete_indicator', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example', models.TextField()),
                ('label', models.CharField(default='', max_length=10)),
                ('complete_indicator', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.Project')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.IntegerField(default=0)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.IntegerField(choices=[(0, 'not sure'), (1, 'female'), (2, 'male')], default=0)),
                ('career', models.IntegerField(default=0)),
                ('approval_rate', models.DecimalField(decimal_places=4, default=0, max_digits=5)),
                ('approval_HIT_number', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.UserProfile'),
        ),
        migrations.AddField(
            model_name='hit',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.Project'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='hit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.HIT'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.UserProfile'),
        ),
    ]
