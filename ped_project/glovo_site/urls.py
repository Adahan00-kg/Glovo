from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'store_detail',StoreDetailViewSet,basename='store_detail')
router.register(r'product_detail',ProductDetailViewSet,basename='product_detail')
router.register(r'combo_owner',ComboUpdateViewSet,basename='combo_owner')


urlpatterns = [
    path('urls/', include(router.urls)),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),

    path('',StoreListViewSet.as_view(),name='store_list'),

    path('store_add/',StoreCreateViewSet.as_view(),name = 'store_create'),

    path('<int:pk>/',StoreDetailGetViewSet.as_view(),name = 'store_get'),


    path('product/',ProductListViewSet.as_view(),name = 'product_list'),

    path('product/<int:pk>/',ProductDetailGetViewSet.as_view(),name = 'product_get'),

    path('product_add/',ProductCreateViewSet.as_view(),name = 'product_put'),

    path('combo/',ComboListViewSet.as_view(),name = 'combo_list'),

    path('combo/<int:pk>/',ComboDetailViewSet.as_view(),name = 'combo_detail'),

    path('combo_add/',ComboCreateViewSet.as_view(),name = 'combo_create'),

    path('order_add/',OrderClientViewSet.as_view(),name = 'order_add'),

    path('cart_add/',CartViewSet.as_view(),name = 'cart_add'),

    path('cart/',CartGetViewSet.as_view(),name = 'cart_get'),

    path('cart_item_check/<int:pk>/',CartItemGetViewSet.as_view(),name = 'cart_item_check'),

    path('cart_item_create/',CartItemCreateViewSet.as_view(),name = 'cart_item_create'),

    path('store_review_add/',StorePutReviewViewSet.as_view(),name = 'store_add'),

    path('store_review_check/',StoreReviewViewSet.as_view(),name = 'store_check'),

    path('store_review_delete/<int:pk>/',StoreDeleteReviewViewSet.as_view(),name = 'store_delete'),

    path('order_add/',OrderClientViewSet.as_view(),name = 'client_order'),

    path('order_update/<int:pk>/',OrderOwnerUpdateViewSet.as_view(),name = 'owner_order_update'),

    path('order_courier/',OrderCourierListViewSet.as_view(),name = 'courier_order_list'),

    path('order_courier/<int:pk>/',OrderCourierDetailViewSet.as_view(),name = 'courier_order_detail'),

    path('order_check/',OrderListViewSet.as_view(),name = 'order_list'),

    path('order_check/<int:pk>/', OrderDetailUpdateViewSet.as_view(), name='order_detail'),

    path('courier/',CourierViewSet.as_view(),name = 'courier'),

    path('category/',CategoryViewSet.as_view(),name = 'category'),

    path('courier_comments_add/',CourierReviewViewSet.as_view(),name = 'courier_commnets_create'),

    path('courier_comments_check/<int:pk>/',CourierReviewCheckViewSet.as_view(),name = 'courier_comments_check')


]