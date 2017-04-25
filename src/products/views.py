from django.db.models import Q, F, Avg, Count
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from analytics.models import TagView

from digitalmarket.mixins import (
        MultiSlugMixin,
        LoginRequiredMixin,
        StaffRequiredMixin,
        AjaxRequiredMixin
        )

from sellers.models import SellerAccount
from sellers.mixins import SellerAccountMixin
from tags.models import Tag

from .forms import ProductAddForm, ProductModelForm
from .mixins import ProductManagerMixin
from .models import Product, ProductLikes, MyProducts


class ProductLikesAjaxView(AjaxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # credit card required **

        user = request.user
        product_id = request.POST.get("product_id")
        rating_value = request.POST.get("rating_value")
        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({}, status=404)

        try:
            product_obj = Product.object.get(id=product_id)
        except:
            product_obj = Product.objects.filter(id=product_id).first()

        rating_obj, rating_obj_created = ProductLikes.objects.get_or_create(
                user=user,
                product=product_obj
                )
        try:
            rating_obj = ProductLikes.objects.get(user=user, product=product_obj)
        except ProductLikes.MultipleObjectsReturned:
            rating_obj = ProductLikes.objects.filter(user=user, product=product_obj).first()
        except:
            # rating_obj = ProductLikes.objects.create(user=user, product=product_obj)
            rating_obj = ProductLikes()
            rating_obj.user = user
            rating_obj.product = product_obj
        rating_obj.rating = int(rating_value)
        myproducts = user.myproducts.products.all()
        if product_obj in myproducts:
            rating_obj.verified = True
        rating_obj.save()

        data = {
            "success": True
        }
        return JsonResponse(data)


class ProductCreateView(SellerAccountMixin, CreateView):
    model = Product
    template_name = "create_view.html"
    form_class = ProductModelForm

    def form_valid(self, form):
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        if tags:
            tags_list = tags.split(",")
            for tag in tags_list:
                if not tag == " ":
                    new_tags = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tags.products.add(form.instance)
        return valid_data

    # this makes it return user profile - but user profile does not exist yet
    def get_success_url(self):
        return reverse("products:list")

class ProductUpdateView(ProductManagerMixin, MultiSlugMixin, UpdateView):
    model = Product
    template_name = "update_view.html"
    form_class = ProductModelForm

    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        return initial

    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        # obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")
            obj = self.get_object()
            obj.tag_set.clear()
            for tag in tags_list:
                if not tag == " ":
                    new_tags = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tags.products.add(self.get_object())
        return valid_data

class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        rating_sum = obj.productlikes_set.aggregate(Count("rating"))
        context["rating_sum"] = rating_sum
        if self.request.user.is_authenticated():
            rating_obj = ProductLikes.objects.filter(user=self.request.user, product=obj)
            if rating_obj.exists():
                context['my_rating'] = rating_obj.first().rating
            for tag in tags:
                new_view = TagView.objects.add_count(self.request.user, tag)
        return context

class VendorListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

    def get_object(self):
        username= self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__username=username)
        return seller

    def get_context_data(self, *args, **kwargs):
        context = super(VendorListView, self).get_context_data(*args, **kwargs)
        context["vendor_name"] = str(self.get_object().user.username)
        return context

	def get_queryset(self, *args, **kwargs):
		seller = self.get_object()
		qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs



class SellerProductListView(SellerAccountMixin, ListView):
    model = Product
    template_name = "sellers/product_list_view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(SellerProductListView, self).get_queryset(**kwargs)
        qs = qs.filter(seller=self.request.user)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)
                ).order_by("title")
        return qs

class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)
                ).order_by("-pk")
        return qs

class UserLibraryListView(LoginRequiredMixin, ListView):
    model = MyProducts
    template_name = "products/library_list.html"

    def get_queryset(self, *args, **kwargs):
        obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
        qs = obj.products.all()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)
                ).order_by("-pk")
        return qs

def create_view(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "create_view.html"
    context = {
            "form" : form,
        }
    return render(request, template, context)

def update_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    template = "update_view.html"
    context = {
        "product" : product,
        "form" : form,
    }
    return render(request, template, context)

def detail_slug_view(request, slug=None):
	product = Product.objects.get(slug=slug)
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()
	# print slug
	# product = 1
	template = "detail_view.html"
	context = {
		"object": product
		}
	return render(request, template, context)

def detail_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    template = "detail_view.html"
    context = {
        "product" : product
    }
    return render(request, template, context)

def list_view(request):
    # multi item
    print request
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset" : queryset
    }
    return render(request, template, context)
