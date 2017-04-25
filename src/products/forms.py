from django import forms
from django.utils.text import slugify

from .models import Product

ITEM_TYPE = (
    ('dance', "Dancewear"),
    ('shoes', "Shoes"),
    ('perf', "Performance/Costume"),
)
CONDITION_TAGS = (
    ('with', "Yes"),
    ('without', "No"),
)
CONDITION_WEAR = (
    ('wear', "Yes"),
    ('nowear', "No"),
)

class ProductAddForm(forms.Form):
    tags = forms.CharField(label='Tags', required=False, widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Listing Title Here",
            }
    ))
    itemType = forms.ChoiceField(label='Item Type', choices=ITEM_TYPE, widget=forms.Select(attrs={'class':'form-control'}))

    brand = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Add Brand Name",
            }
    ))
    title = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Listing Title Here",
            }
    ))
    slug = forms.SlugField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Add a custom URL (if it's available!)",
            }
    ))
    style = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "What type of garment or shoe is this?",
            }
    ))
    size = forms.CharField(widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "What size is the item?",
            }
    ))
    color = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "What color is the item?",
            }
    ))
    description = forms.CharField(widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Describe how you might wear this, for what type of dance, and the condition of the garment or shoes!",
            }
    ))
    price = forms.DecimalField(widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "How much do you want to charge?",
            }
    ))
    sale_price = forms.DecimalField(widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "If your item goes on sale, what's the lowest price you are willing to take?",
            }
    ))
    msrp = forms.DecimalField(label='Retail Price', widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "What does this item usually sell for?",
            }
    ))
    conditionTags = forms.ChoiceField(label='Does this item still have retail tags attached?', choices=CONDITION_TAGS, widget=forms.Select(attrs={'class':'form-control'}))

    conditionWear = forms.ChoiceField(label='Does this item have any signs of wear?', choices=CONDITION_WEAR, widget=forms.Select(attrs={'class':'form-control'}))


class ProductModelForm(forms.ModelForm):
    tags = forms.CharField(label='Tags', required=False, widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Listing Title Here",
            }
    ))
    conditionTags = forms.ChoiceField(label='Does this item still have retail tags attached?', choices=CONDITION_TAGS, widget=forms.Select(attrs={'class':'form-control'}))

    conditionWear = forms.ChoiceField(label='Does this item have any signs of wear?', choices=CONDITION_WEAR, widget=forms.Select(attrs={'class':'form-control'}))

    itemType = forms.ChoiceField(label='Item Type', choices=ITEM_TYPE,              widget=forms.Select(attrs={'class':'form-control'}))

    brand = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Add Brand Name",
            }
    ))
    title = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Listing Title Here",
            }
    ))
    # slug = forms.SlugField(widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Add a custom URL (if it's available!)",
    #         }
    # ))
    color = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "What color is the item?",
            }
    ))
    style = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "What type of garment or shoe is this?",
            }
    ))
    size = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "What size is it?",
            }
    ))
    description = forms.CharField(widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Describe how you might wear this, for what type of dance, and the condition of the garment or shoes!",
            }
    ))
    price = forms.DecimalField(widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "How much do you want to charge?",
            }
    ))
    sale_price = forms.DecimalField(widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "If your item goes on sale, what's the lowest price you are willing to take?",
            }
    ))
    msrp = forms.DecimalField(label='Retail Price', widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "What does this item usually sell for?",
            }
    ))
    # media = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = Product
        fields = [
            "brand",
            # "media",
            "title",
            "description",
            "price",
            "color",
            "itemType",
            "style",
            "size",
            "sale_price",
            "msrp",
            "conditionTags",
            "conditionWear",
        ]

    def clean(self, *args, **kwargs):
        cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
        # title = cleaned_data.get("title")
        # slug = slugify(title)
        # qs = Product.objects.filter(slug=slug).exists()
        # if qs:
        #     raise forms.ValidationError("Title Taken, a new title is needed!")
        # return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 2.00:
            raise forms.ValidationError("Price must be greater than $2.00!")
        else:
            return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 5:
            return title
        else:
            raise forms.ValidationError("Please create a more descriptive title!")
