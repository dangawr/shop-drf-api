from rest_framework import serializers
from core.models import Product, Category, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='shop:product-detail'
    )
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'products', 'products_count',)
        read_only_fields = ('id', 'count',)

    def get_products_count(self, obj):
        counter = Product.objects.filter(categories=obj).count()
        return counter


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created', 'is_available')

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        product = Product.objects.create(**validated_data)
        for category in categories:
            category_object, created = Category.objects.get_or_create(**category)

            product.categories.add(category_object)

        return product


class ProductOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'price')
        read_only_fields = ('id', 'name', 'price')


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')

    def create(self, validated_data):
        cart, created = Cart.objects.get_or_create(user=self.context['request'].user)
        return CartItem.objects.create(cart=cart, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductOrderItemSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_items', 'total_price', 'created_at', 'updated_at')
        read_only_fields = fields

    def get_total_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj.pk)
        total = 0
        for order_item in order_items:
            total += (order_item.product.price * order_item.quantity)
        return total

    def create(self, validated_data):
        try:
            cart = Cart.objects.get(user=self.context['request'].user)
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)
        order = Order.objects.create(user=self.context['request'].user)
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(product=cart_item.product, quantity=cart_item.quantity, order=order)
        return order

