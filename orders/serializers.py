# serializers.py
from rest_framework import serializers
from .models import Customer, Product, Category 
from .models import Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'date_joined',
            'code',
            'bio'
        ]
        read_only_fields = ['id', 'date_joined']
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  # This assumes your Category model has a `__str__` method for representation

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'price',
            'slug',
            'image',
            'description',
            'label',
            'available',
            'created',
            'updated',
            'stock'
        ]
        read_only_fields = ['id', 'created', 'updated']
