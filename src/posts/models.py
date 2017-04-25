from django.conf import settings
from django.db import models

from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify


def media_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to=media_location,
        # storage = FileSystemStorage(location=settings.PROTECTED_ROOT)
        )
    body = models.TextField()
    slug = models.SlugField(blank=True, unique="True")
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]

    def get_absolute_url(self):
        view_name = "post_detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def post_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(post_pre_save_reciever, sender=Post)
