from rest_framework import serializers

from .models import *

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
        fields = ['first_name','last_name']# # для комента


class StoreReviewSerializer(serializers.ModelSerializer):
    author = UserReviewSerializer(read_only=True)
    created_time = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = StoreReview
        fields = ['author','text',
                  'stars','parent_review','created_time']


class StorePutReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = ['author','store_rating','text',
                  'stars','parent_review']


class StoreImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImg
        fields = ['store_photo']


class StoreListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = ['id','store_name','store_photo','average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImg
        fields = ['product_img']


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ProductListSerializer(serializers.ModelSerializer):
    category_product = CategoryProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ['product_name','category_product',
                  'product_description','product_price','product_images','active']


class ProductPutSerializer(serializers.ModelSerializer):
    photo = ProductImgSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = ['store_product','product_name','category_product',
                  'product_description','product_price',
                  'product_images','photo','active']


class ProductDetailSerializer(serializers.ModelSerializer):
    photo = ProductImgSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = ['product_name','category_product',
                  'product_description','product_price',
                  'product_images','photo','active']


class CategorySerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True,many=True)
    class Meta:
        model = Category
        fields = ['category_name','product']


class ComboProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    class Meta:
        model = ComboProduct
        fields = ['product', 'quantity_products']
# many True Ну очурсом ошибка чыгып калтат detail га кирсем
# жазсам list те ошибка чыгып калтат
# все решил ...


class ComboListSerializer(serializers.ModelSerializer):
    products = ComboProductSerializer(source='comboproduct_set', many=True)
    category_combo = CategorySerializer(many=True)
    class Meta:
        model = Combo
        fields = ['combo_name',  'products','category_combo','combo_price']


class ComboDetailSerializer(serializers.ModelSerializer):
    products = ComboProductSerializer()
    class Meta:
        model = Combo
        fields = ['combo_name','store_combo', 'combo_description',
                  'products','category_combo','combo_price'] # агай ушул жер под вопросом иштеп атат озу бирок есть  вопросы . тура эмес кошулуп атат combo


class ComboCreateSerializer(serializers.ModelSerializer):
    products = ComboProductSerializer(source='comboproduct_set', many=True)
    class Meta:
        model = Combo
        fields = ['combo_name','store_combo', 'combo_description',
                  'products','category_combo','combo_price']


class CartItemGetSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    combo = ComboListSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['product', 'product_quantity', 'combo_quantity', 'combo','total_price'] # combo менен product кошкондо даяр продукт эмес башка тандоолор чыгып атат не понял в чем дело


    def get_total_price(self,obj):
        return obj.get_total_price()


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart','product','combo','product_quantity','combo_quantity']



class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user']


class CartGetSerializer(serializers.ModelSerializer):
    items =CartItemGetSerializer(read_only=True,many=True)
    class Meta:
        model = Cart
        fields = ['user','items']



class CourierReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierReview
        fields = ['author','text','stars',
                  'created_time','courier_rating']

class CourierSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    courier_ratings = CourierReviewSerializer(read_only=True,many=True)
    user_courier = UserReviewSerializer()

    class Meta:
        model = Courier
        fields = ['user_courier','average_rating','courier_ratings','current_orders']


    def get_average_rating(self, obj):
        return obj.get_average_rating()




class OrderPutSerializer(serializers.ModelSerializer):
    current_orders = CourierSerializer(read_only=True,many=True)
    class Meta:
        model = Order
        fields = ['user','cart','address','current_orders']


class OrderOwnerSerializer(serializers.ModelSerializer):
    current_orders = CourierSerializer(read_only=True,many=True)
    class Meta:
        model  = Order
        fields = ['user','cart','created_date',
                  'address','current_orders']


class  CheckOrderSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer()
    cart = CartItemGetSerializer()
    created_date = serializers.DateTimeField(format='%d - %m - %Y  %H:%M')
    current_orders = CourierSerializer(read_only=True,many=True)
    courier = CourierSerializer()
    class Meta:
        model = Order
        fields = ['user','cart','created_date',
                  'address','current_orders','status_order','courier']


class  OrderCourierSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)
    cart = CartItemGetSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d - %m - %Y  %H:%M')
    current_orders = CourierSerializer(read_only=True,many=True)
    class Meta:
        model = Order
        fields = ['user','cart','created_date',
                  'address','current_orders','status_order','courier']






class StoreDetailSerializer(serializers.ModelSerializer):
    store_img = StoreImgSerializer(read_only=True,many=True)
    store_rating = StoreReviewSerializer(read_only=True,many=True)
    average_rating = serializers.SerializerMethodField()
    owner = UserReviewSerializer()
    store_product = ProductListSerializer(read_only=True,many=True)
    store_combo = ComboListSerializer(read_only=True,many=True)

    class Meta:
        model = Store
        fields = ['store_name','store_img','description_store',
                  'contact_info','store_rating','address','owner',
                  'average_rating','store_product','store_combo']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name','description_store',
                  'contact_info','address','owner','store_photo']


