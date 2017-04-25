# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20170415_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photos',
            field=models.FileField(upload_to=b'/static/'),
        ),
    ]
