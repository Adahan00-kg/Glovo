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
    role = models.CharField(max_length=25,choices=ROLE_CHOICES,default='клиент')
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


class StoreImg(models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store_img')
    store_photo = models.ImageField(upload_to='store_photo/')



class Category(models.Model):
    category_name = models.CharField(max_length=16)
    store_category = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store_category')

    def __str__(self):
        return self.category_name





class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ManyToManyField(Category,related_name='product')
    product_description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    store_product  = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='store')
    product_images = models.FileField(upload_to='product_vid/')
    active  = models.BooleanField(default=True,verbose_name='в наличии')

    def __str__(self):
        return f'{self.product_name}'


class ProductImg(models.Model):
    product_photo = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='photo')
    product_img = models.ImageField(upload_to='product_img/')



class Review(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product_ratting = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product',null=True,blank=True)
    courier_rating = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='курьер',null=True,blank=True,related_name='courier_ratings')
    store_rating = models.ForeignKey(Store,on_delete=models.CASCADE,verbose_name='магазин',null=True,blank=True,related_name='store_rating')
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=[(i ,str(i)) for i in range(6)],verbose_name='Рейтинг',null=True,blank=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.author} - {self.text}'













class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveSmallIntegerField(choices=[(i ,str(i)) for i in range(10000)],verbose_name='количеста',null=True,blank=True)



    def get_total_price(self):
        return self.product.price * self.quantity




class Order(models.Model):
    user =  models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=55)




class Courier(models.Model):
    user_courier = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    STATUS_ORDER = (
        ('ожидания','ожидания'),
        ('в пути','в пути'),
        ('доставлено','доставлено')
    )
    status_book = models.CharField(max_length=25,choices=STATUS_ORDER)



    def __str__(self):
        return f'{self.user_courier.first_name} - {self.user_courier.last_name}'
