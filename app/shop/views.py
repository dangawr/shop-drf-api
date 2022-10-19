from rest_framework import viewsets, generics
from core.models import Product, Category, CartItem, Cart, Order
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer, CartSerializer, OrderSerializer
from .permissions import IsOwnerOrStaff, IsStaffOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import filters


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['name', 'categories']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['quantity', 'price']

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)


class CartApiView(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrStaff]


