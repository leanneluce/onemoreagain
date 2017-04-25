from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView

from tags.models import Tag
from products.models import Product
from .models import Post


def home(request):
    posts = Post.objects.order_by('-pub_date')
    queryset = Post.objects.all()
    template = "posts/list_view.html"
    product = None
    products = Product.objects.all()

    context = {
            "posts" : queryset,
            "products" : products,
        }
    return render(request, template, context)

def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    product = None
    products = Product.objects.all()
    template = "posts/detail_view.html"
    tags = Tag.objects.all()

    context = {
            "post" : post,
            "products" : products,
            "tags": tags,
        }

    return render(request, template, context)

def post_detail_slug(request, slug=None):
	post = Post.objects.get(slug=slug)
	try:
		post = get_object_or_404(Post, slug=slug)
	except Post.MultipleObjectsReturned:
		post = Post.objects.filter(slug=slug).order_by("-title").first()
	# print slug
	# product = 1
	template = "posts/detail_view.html"
	context = {
		"object": post
		}
	return render(request, template, context)
