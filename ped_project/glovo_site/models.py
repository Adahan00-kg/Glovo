from django.contrib.auth.models import AbstractUser

from django.db import models

from django.core.validators import MaxValueValidator,MinValueValidator


from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(region='KG',null=True,blank=True)
    ROLE_CHOICES = (
        ('клиент','клиент'),
        ('курьер','курьер'),
        ('владелец магазина','владелец магазина'),
    )
    role =  models.CharField(max_length=25,choices=ROLE_CHOICES,default='клиент')
    age = models.PositiveSmallIntegerField(null=True,blank=True,validators=[MinValueValidator(16),MaxValueValidator(100)])

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Store(models.Model):
    store_name = models.CharField(max_length=30)
    description_store = models.TextField()
    contact_info = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    store_photo = models.FileField(upload_to='store_img/')

    def __str__(self):
        return f'{self.store_name}'

    def get_average_rating(self):
        ratings = self.store_rating.all()
        if ratings.exists():
            return (round(sum(rating.stars for rating in ratings) / ratings.count(), 1))
        return 0

class StoreImg(models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store_img')
    store_photo = models.ImageField(upload_to='store_photo/')



class Category(models.Model):
    category_name = models.CharField(max_length=16)

    def __str__(self):
        return self.category_name





class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category_product = models.ManyToManyField(Category,related_name='category_product')
    product_description = models.TextField()
    product_price = models.PositiveIntegerField(default=0)
    store_product  = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store_product')
    product_images = models.FileField(upload_to='product_vid/')
    active  = models.BooleanField(default=True,verbose_name='в наличии')

    def __str__(self):
        return f'{self.product_name}'





class ProductImg(models.Model):
    product_photo = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='photo')
    product_img = models.ImageField(upload_to='product_img/')



class StoreReview(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    store_rating = models.ForeignKey(Store,on_delete=models.CASCADE,verbose_name='магазин',related_name='store_rating')
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=[(i ,str(i)) for i in range(6)],verbose_name='Рейтинг',null=True,blank=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.author} - {self.text} - {self.store_rating}'






class Combo(models.Model):# XXL
    combo_name = models.CharField(max_length=55)
    store_combo = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store_combo')
    combo_description = models.TextField()
    products = models.ManyToManyField(Product, through='ComboProduct')
    category_combo = models.ManyToManyField(Category,related_name='category_combo')
    combo_price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.combo_name} - {self.combo_price}'


class ComboProduct(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)#XXL shaurma
    quantity_products = models.PositiveIntegerField(default=1) # 3

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity_products}"

class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, null=True, blank=True)
    product_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество продуктов')
    combo_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество комбо продуктов')

    def __str__(self):
        return f'{self.cart} - {self.product} - {self.combo}'

    def get_total_price(self):
        total = 0
        if self.product:
            total += self.product.product_price * self.product_quantity

        if self.combo:
            total += self.combo.combo_price * self.combo_quantity

        return total
# количества боюнча скидка

class Order(models.Model):
    user =  models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_order')
    cart = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=55)
    STATUS_ORDER = (
        ('ожидания','ожидания'),
        ('В процессе  доставки.','В процессе доставки.'),
        ('доставлено','доставлено'),
        ('Отменен','Отменен')
    )
    status_order = models.CharField(max_length=25,choices=STATUS_ORDER,default='ожидания')
    courier = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='courier_order',null=True,blank=True)

    def __str__(self):
        return f'{self.user} - {self.cart} - {self.status_order}'

class Courier(models.Model):
    user_courier = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    STATUS_COURIER = (
        ('свободен','свободен'),
        ('занят','занят'),
        ('не на работе','не на работе') ,

    )
    status_courier = models.CharField(max_length=25,choices=STATUS_COURIER,default='свободен')
    current_orders = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='current_orders',null=True,blank=True)


    def get_average_rating(self):
        ratings = self.courier_ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0




    def __str__(self):
        return f'{self.status_courier} - {self.user_courier} - {self.current_orders}'




class CourierReview(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='author')
    courier_rating = models.ForeignKey(Courier,on_delete=models.CASCADE,verbose_name='курьер',null=True,blank=True,related_name='courier_ratings')
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=[(i ,str(i)) for i in range(6)],verbose_name='Рейтинг',null=True,blank=True)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.text} - {self.courier_rating}'
