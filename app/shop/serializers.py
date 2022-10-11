from rest_framework import serializers
from core.models import Product, Category


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
