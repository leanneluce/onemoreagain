from django.conf import settings
from django.core.files.storage import FileSystemStorage
# for protected media:
# from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from sellers.models import SellerAccount

def media_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
    itemType = models.CharField(max_length=40)
    media = models.ImageField(
            blank=True,
            null=True,
            upload_to=media_location,
            storage = FileSystemStorage(location=settings.MEDIA_ROOT)
            )
    brand = models.CharField(max_length=40)
    color = models.CharField(max_length=40)
    title = models.CharField(max_length=80)
    slug = models.SlugField(blank=True, unique="True")
    style = models.CharField(max_length=40)
    size = models.CharField(max_length=40)
    description = models.TextField(default="True")
    price = models.DecimalField(max_digits=100, decimal_places=2, default=8.88)
    sale_active = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.88)
    msrp = models.DecimalField(max_digits=100, decimal_places=2, default=8.88)
    conditionTags = models.CharField(max_length=40)
    conditionWear = models.CharField(max_length=40)

    def __unicode__(self):
        return self.title

    # dynamically updates urls - so that if the name is changes in urls.py - the whole thing gets updated
    def get_absolute_url(self):
        view_name = "products:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_edit_url(self):
		view_name = "sellers:product_edit"
		return reverse(view_name, kwargs={"pk": self.id})

    @property
    def get_price(self):
        if self.sale_price and self.sale_active:
            return self.sale_price
        else:
            return self.price

    def get_html_price(self):
        price = self.get_price
        if price == self.sale_price:
            return "<span>$%s</span> <br/><strong>Originally: $%s</strong>" %(self.sale_price, self.price)
        else:
            return "$%s" %(self.price)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)



def thumbnail_location(instance, filename):
    return "%s/%s" %(instance.product.slug, filename)

THUMB_CHOICES = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)
class Thumbnail(models.Model):
    product = models.ForeignKey(Product)
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
        width_field = "width",
        height_field = "height",
        upload_to=thumbnail_location,
        # storage = FileSystemStorage(location=settings.PROTECTED_ROOT)
    )

    def __unicode__(self):
        return str(self.media.path)

import os
import shutil
from PIL import Image
import random

from django.core.files import File

def create_new_thumb(media_path, instance, owner_slug, max_length, max_width):
        filename = os.path.basename(media_path)
        thumb = Image.open(media_path)
        size = (max_length, max_width)
        thumb.thumbnail(size, Image.ANTIALIAS)

        temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, owner_slug)

        if not os.path.exists(temp_loc):
            os.makedirs(temp_loc)

        temp_file_path = os.path.join(temp_loc, filename)
        if os.path.exists(temp_file_path):
            temp_path = os.path.join(temp_loc, "%s" %(random.random()))
            os.makedirs(temp_path)
            temp_file_path = os.path.join(temp_path, filename)

        temp_image = open(temp_file_path, "w")
        thumb.save(temp_image)
        temp_data = open(temp_file_path, "r")

        thumb_file = File(temp_data)
        instance.media.save(filename, thumb_file)
        shutil.rmtree(temp_loc, ignore_errors=True)
        return True

def product_post_save_receiver(sender, instance, *args, **kwargs):
    if instance.media:
        hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
        sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
        micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

        hd_max = (800, 800)
        sd_max = (600, 600)
        micro_max = (200, 200)

        media_path = instance.media.path
        owner_slug = instance.slug
        if hd_created:
            create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])

        if sd_created:
            create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])

        if micro_created:
            create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])

post_save.connect(product_post_save_receiver, sender=Product)

class MyProducts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product, blank=True)


    def __unicode__(self):
        return "%s" %(self.products.count())

    class Meta:
        verbose_name = "My Products"
        verbose_name_plural = "My Products"

class ProductLikes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    rating = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" %(self.rating)
