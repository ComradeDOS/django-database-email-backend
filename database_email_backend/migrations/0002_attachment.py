# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-11 12:44
from __future__ import unicode_literals

import database_email_backend.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_email_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('content_base64', database_email_backend.fields.Base64Field(blank=True, db_column='content', default=None, null=True)),
                ('mimetype', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='database_email_backend.Email')),
            ],
        ),
    ]
