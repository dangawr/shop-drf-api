from rest_framework import viewsets, generics
from core.models import Product, Category, CartItem, Cart, Order
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer, CartSerializer, OrderSerializer, OrderUpdateSerializer
from .permissions import IsStaffOrReadOnly, IsStaff
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['name', 'categories']
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)


class CartApiView(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'update': (IsStaff,),
        'destroy': (IsStaff,)
    }

    def get_serializer_class(self):
        if self.action == 'update':
            return OrderUpdateSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
