from rest_framework import viewsets, generics, mixins
from core.models import Product, Category, CartItem, Cart, Order
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CartItemSerializer,
    CartSerializer,
    OrderSerializer,
    OrderUpdateSerializer)
from .permissions import IsStaffOrReadOnly, IsStaff
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    description='Endpoint for products. You can search by name or categories(put ids of categories) and order by '
                'quantity or price.',
    methods=["GET"]
)
@extend_schema(
    description='This methods are allowed only for staff users.', methods=["POST", "PUT", "PATCH", "DELETE"]
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['name', 'categories']
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['quantity', 'price']

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


@extend_schema(
    description='Endpoint for categories.',
    methods=["GET"]
)
@extend_schema(
    description='This methods are allowed only for staff users.', methods=["POST", "PUT", "PATCH", "DELETE"]
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class CartItemViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """
    Endpoint for adding or editing items to cart.
    Please type product id and quantity. Cart is auto-deleted when order is created.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)


class CartApiView(generics.RetrieveDestroyAPIView):
    """
    Endpoint for check products in cart.
    To add products, please use Cart-Item endpoint.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


@extend_schema_view(
    list=extend_schema(description="Endpoint for check all user's orders."),
    retrieve=extend_schema(description='Endpoint for check order detail'),
    create=extend_schema(description='Endpoint for create order from cart.'),
    update=extend_schema(description='This method is allowed only for staff users'),
    partial_update=extend_schema(description='This method is allowed only for staff users'),
    destroy=extend_schema(description='This method is allowed only for staff users')
)
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
