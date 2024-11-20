from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'<int:pk>',StoreDetailViewSet,basename='store_detail')
router.register(r'review',ReviewViewSet,basename='review')
router.register(r'product_detail',ProductDetailViewSet,basename='product_detail')
router.register(r'category',CategoryViewSet,basename='category')
router.register(r'cart',CategoryViewSet,basename='cart')
router.register(r'order',OrderViewSet,basename='order')
router.register(r'courier',CourierViewSet,basename='courier')


urlpatterns = [
    path('urls/', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('',StoreListViewSet.as_view(),name='store_list')


]