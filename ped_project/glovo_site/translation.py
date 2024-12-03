from .models import Product,Category,Store
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description')



@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('description_store',)