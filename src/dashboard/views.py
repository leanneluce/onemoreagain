import random

from django.views.generic import View
from django.shortcuts import render

from products.models import Product
from posts.models import Post

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        tag_views = None
        products = None
        posts = None
        queryset = Post.objects.all()
        queryset = queryset[:2]

        top_tags = None
        try:
            tag_views = request.user.tagview_set.all().order_by("-count")
        except:
            pass

        owned = None

        try:
            owned = request.user.myproducts.products.all()
        except:
            pass

        if tag_views:
            top_tags = [x.tag for x in tag_views]
            products = Product.objects.filter(tag__in=top_tags)
            if owned:
                products = products.exclude(pk__in=owned)

            if products.count() < 10:
                products = Product.objects.all().order_by("?")
                if owned:
                    products = products.exclude(pk__in=owned)
                products = products[:3]
            else:
                products = products.distinct()
                products = sorted(products, key= lambda x: random.random())

        context = {
            "products": products,
            "top_tags": top_tags,
            "posts": queryset,
        }
        return render(request, "dashboard/view.html", context)
