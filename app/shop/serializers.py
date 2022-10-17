from rest_framework import serializers
from core.models import Product, Category, Cart, CartItem


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


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source='product.id', read_only=True)
    cart = serializers.IntegerField(source='cart.id', read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemCreateSerializer(serializers.ModelSerializer):
    PRODUCT_CHOICES = [product.pk for product in Product.objects.all()]
    CART_CHOICES = [cart.pk for cart in Cart.objects.all()]
    product = serializers.ChoiceField(choices=PRODUCT_CHOICES, write_only=True)
    cart = serializers.ChoiceField(choices=CART_CHOICES, write_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.get(pk=validated_data.pop('product'))
        cart = Cart.objects.get(pk=validated_data.pop('cart'))
        return CartItem.objects.create(product=product, cart=cart, **validated_data)

    def update(self, instance, validated_data):
        product_id = validated_data.pop('product', None)
        cart_id = validated_data.pop('cart', None)
        if product_id is not None:
            product = Product.objects.get(pk=product_id)
            instance.product = product
        if cart_id is not None:
            cart = Cart.objects.get(pk=cart_id)
            instance.cart = cart
        instance.save()
        return instance
