from django.contrib import admin

# Register your models here.
from .models import Product, MyProducts, Thumbnail, ProductLikes

class ThumbnailInline(admin.TabularInline):
    extra = 1
    model = Thumbnail

class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]
    list_display = ["__str__", "brand", "title", "style", "price", "msrp", "sale_price", "size"]
    search_fields = ["brand", "title", "style", "title"]
    list_filter = ["price", "brand", "size"]
    list_editable = ["sale_price"]
    # prepopulated_fields = {"slug": ("title",)}
    # above dictates what is showing in the django admin panel! :-)
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

admin.site.register(MyProducts)

admin.site.register(Thumbnail)

admin.site.register(ProductLikes)
