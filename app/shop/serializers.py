from rest_framework import serializers
from core.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created', 'is_available']

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        product = Product.objects.create(**validated_data)
        for category in categories:
            category_object, created = Category.objects.get_or_create(**category)

            product.categories.add(category_object)

        return product
