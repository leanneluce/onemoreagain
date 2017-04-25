# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('pub_date', models.DateTimeField()),
                ('image', models.ImageField(upload_to=posts.models.media_location)),
                ('body', models.TextField()),
            ],
        ),
    ]
