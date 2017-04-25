# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import products.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0024_auto_20170418_0508'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLikes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/leanneluce/Documents/marketplace/dm/static_cdn/media'), null=True, upload_to=products.models.media_location, blank=True),
        ),
        migrations.AddField(
            model_name='productlikes',
            name='product',
            field=models.ForeignKey(to='products.Product'),
        ),
        migrations.AddField(
            model_name='productlikes',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
