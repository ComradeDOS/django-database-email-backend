# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 11:24
from __future__ import unicode_literals

import database_email_backend.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database_email_backend', '0002_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='content_base64',
        ),
        migrations.AddField(
            model_name='attachment',
            name='content',
            field=database_email_backend.fields.Base64Field(blank=True, db_column='content', default=None, null=True),
        ),
    ]
