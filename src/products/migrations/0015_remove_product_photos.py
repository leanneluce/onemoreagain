# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20170416_0239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='photos',
        ),
    ]
