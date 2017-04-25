# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_product_sale_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user',
            new_name='seller',
        ),
        migrations.RemoveField(
            model_name='product',
            name='managers',
        ),
    ]
