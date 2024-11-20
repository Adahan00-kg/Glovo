from itertools import product

from rest_framework import serializers


from .models import *

from .models import *

from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password','first_name', 'last_name', 'age',
         'phone_number','role']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username','first_name', 'last_name', 'phone_number']

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']

class ReviewSerializer(serializers.ModelSerializer):
    author = UserReviewSerializer()
    class Meta:
        model = Review
        fields = ['author','product_ratting','courier_rating',
                  'store_rating']


class StoreImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImg
        fields = ['store_photo']


class StoreDetailSerializer(serializers.ModelSerializer):
    store_img = StoreImgSerializer(read_only=True,many=True)
    class Meta:
        model = Store
        fields = ['store_name','store_photo','store_img','description_store',
                  'contact_info','address','owner']

class StoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name','store_photo']




class ProductImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImg
        fields = ['product_img']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name','category',
                  'product_description','price','product_images','active']


class ProductDetailSerializer(serializers.ModelSerializer):
    product = ReviewSerializer(read_only=True,many=True)
    photo = ProductImgSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = ['product_name','category',
                  'product_description','price',
                  'product_images','photo','active','product']


class CategorySerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True,many=True)
    class Meta:
        model = Category
        fields = ['category_name','store_category','product']







class CartSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    class Meta:
        model = Cart
        fields = ['user','product','quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart = CartSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Order
        fields = ['user','cart','created_date','address']



class CourierSerializer(serializers.ModelSerializer):
    user_courier = UserSerializer()
    order = OrderSerializer(many=True)
    class Meta:
        model = Courier
        fields = ['user_courier','cart_courier']


