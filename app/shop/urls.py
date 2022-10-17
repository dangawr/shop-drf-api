from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'shop'

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('cart-items', views.CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', views.CartApiView.as_view(), name='cart')
]
