from django.contrib import admin
from .models import User, Product, Category, CartItem, Cart, Order, OrderItem


class UserAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class CartItemAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    pass


class OrderItemAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)