from django.contrib import admin
from .models import *
from django.contrib import admin

class StorePhotoInlines(admin.TabularInline):
    model = StoreImg
    extra = 1

class StoreAdmin(admin.ModelAdmin):
    inlines = [StorePhotoInlines]

class ProductImgInlines(admin.TabularInline):
    model = ProductImg
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgInlines]


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
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)