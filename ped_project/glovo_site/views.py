from rest_framework import viewsets,permissions,status,generics
from rest_framework.permissions import IsAdminUser
from urllib3 import request

from .filters import ProductFilter
from .serializer import *

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .permission import *


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class StorePutReviewViewSet(generics.CreateAPIView):
    queryset = StoreReview.objects.all()
    serializer_class = StorePutReviewSerializer
    permission_classes = [OwnerReview,CheckCourier]


class StoreReviewViewSet(generics.ListAPIView):
    queryset = StoreReview.objects.all()
    serializer_class = StoreReviewSerializer
    permission_classes = [permissions.IsAuthenticated,CheckReview]# агайдан надо  уточнить как чтоб только свои review видеть

class StoreDeleteReviewViewSet(generics.RetrieveDestroyAPIView):
    queryset = StoreReview.objects.all()
    serializer_class = StoreReviewSerializer
    permission_classes = [CheckReview,CheckCourier]



class CourierReviewViewSet(generics.CreateAPIView):
    queryset = CourierReview.objects.all()
    serializer_class = CourierReviewSerializer
    permission_classes = [OwnerReview,CheckCourier]


class CourierReviewCheckViewSet(generics.RetrieveDestroyAPIView):
    queryset = CourierReview.objects.all()
    serializer_class = CourierReviewSerializer
    permission_classes = [OwnerReview,CheckReview,CheckCourier]


class StoreListViewSet(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,]
    search_fields = ['store_name']
    permission_classes = [CheckCourier,CheckCourier]


class StoreCreateViewSet(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [CheckOwner,CheckCourier]


class StoreDetailViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer
    permission_classes = [OwnerStoreUpdate,CheckCourier]


class StoreDetailGetViewSet(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class ProductListViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    filterset_class = ProductFilter

class ProductDetailGetViewSet(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [CheckCourier]


class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [OwnerProductUpdate]

class ProductCreateViewSet(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductPutSerializer
    permission_classes = [CheckOwner]

class CategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CheckCourier]


class CartViewSet(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [CheckCourier]

class CartGetViewSet(generics.ListAPIView):
    serializer_class = CartGetSerializer


    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)


class CartItemGetViewSet(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemGetSerializer # нужно даработка
    permission_classes = [CheckCourier]


class CartItemCreateViewSet(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class OrderClientViewSet(generics.ListCreateAPIView):

    serializer_class = OrderPutSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminUser,OwnerReview]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)

class OrderOwnerUpdateViewSet(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOwnerSerializer
    permission_classes = [OrderOwner]


class OrderListViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = CheckOrderSerializer
    permission_classes = [OrderOwner]


class OrderDetailUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = CheckOrderSerializer
    permission_classes = [CheckClient]


class OrderCourierListViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCourierSerializer
    permission_classes = [CheckClient]


class OrderCourierDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCourierSerializer
    permission_classes = [CourierCheck]


class CourierViewSet(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class ComboListViewSet(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboListSerializer
    permission_classes = [permissions.IsAdminUser]

class ComboDetailViewSet(generics.RetrieveAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboDetailSerializer


class ComboUpdateViewSet(viewsets.ModelViewSet):
    queryset = Combo.objects.all()
    serializer_class = ComboDetailSerializer
    permission_classes = [permissions.IsAdminUser,ComboOwner]


class ComboCreateViewSet(generics.CreateAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboDetailSerializer
    permission_classes = [CheckOwner]




