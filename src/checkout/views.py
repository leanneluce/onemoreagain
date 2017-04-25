import datetime

from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from django.shortcuts import render

from products.models import Product, MyProducts
from digitalmarket.mixins import AjaxRequiredMixin
from billing.models import Transaction

class CheckoutAjaxView(AjaxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # credit card required **

        user = request.user
        product_id = request.POST.get("product_id")
        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({}, status=404)

        try:
            product_obj = Product.object.get(id=product_id)
        except:
            product_obj = Product.objects.filter(id=product_id).first()

        # run transaction
        trans_obj = Transaction.objects.create(
                user = request.user,
                product = product_obj,
                price = product_obj.get_price,
            )

        my_products = MyProducts.objects.get_or_create(user=request.user)[0]
        my_products.products.add(product_obj)

        data = {
            "works": True,
            "time": datetime.datetime.now(),
        }
        return JsonResponse(data)


class CheckoutTestView(View):
    def post(self, request, *args, **kwargs):
        print request.POST.get("testData")
        if request.is_ajax():
            data = {
                "works" : True,
                "time" : datetime.datetime.now(),
            }
            return JsonResponse(data)
        return HttpResponse("Hello There!")

    def get(self, request, *args, **kwargs):
        template = "checkout/test.html"
        context = {}
        return render(request, template, context)
