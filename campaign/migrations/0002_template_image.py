# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 16:54
from __future__ import unicode_literals

import campaign.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='image',
            field=models.ImageField(null=True, upload_to=campaign.models.get_templatesimage_path),
        ),
    ]
