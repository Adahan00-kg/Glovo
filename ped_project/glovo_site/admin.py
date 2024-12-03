from .models import *



from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


class ProductImgInlines(admin.TabularInline):
    model = ProductImg
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgInlines]
# @admin.register(Product)
# class ProductAdmin(TranslationAdmin):
#     inlines = [ProductImgInlines]
#     class Media:
#         js = (
#             'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
#             'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
#             'modeltranslation/js/tabbed_translation_fields.js',
#         )
#         css = {
#             'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
#         }


class StorePhotoInlines(admin.TabularInline):
    model = StoreImg
    extra = 1

class StoreAdmin(admin.ModelAdmin):
    inlines = [StorePhotoInlines]


class CompoProductInlines(admin.TabularInline):
    model = ComboProduct
    extra = 1


class ComboAdmin(admin.ModelAdmin):
    inlines = [CompoProductInlines]

admin.site.register(Product,ProductAdmin)
admin.site.register(Store,StoreAdmin)
admin.site.register(Combo,ComboAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Courier)
admin.site.register(StoreReview)
admin.site.register(CourierReview)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)