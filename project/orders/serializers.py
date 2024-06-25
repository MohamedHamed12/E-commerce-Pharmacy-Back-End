# -*- coding: utf-8 -*-
from products.models import *
from products.serializers import *
from rest_framework import serializers

from .models import *

# class PaymobOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymobOrder
#         fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True ,read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['user', 'created_at', 'updated_at','total_price','status']

class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    # product = serializers.StringRelatedField()

    class Meta:
        model =CartItem
        fields='__all__'
        extra_fields =['product_name']
        # fields=['id','product','product_name','quantity','cart']


class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer(source='cart__items', many=True, read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model =Cart
        fields='__all__'
        # fields=['id','user','items']
        extra_fields =['items']


# class CreatePaymobOrderSerializer(serializers.Serializer):
#     order_id = serializers.CharField()
#     def validate_order_id(self, value):
#         try:
#             order = Order.objects.get(id=value)
#         except Order.DoesNotExist:
#             raise serializers.ValidationError("Order does not exist.")
#         return order

# class CreatePaymobOrderSerializer(serializers.Serializer):
#     order_id = serializers.CharField()
#     def validate_order_id(self, value):
#         try:
#             order = Order.objects.get(id=value)
#         except Order.DoesNotExist:
#             raise serializers.ValidationError("Order does not exist.")
#         return order

class PaymobOrderSerializer(serializers.ModelSerializer):
    paymob_order_id=serializers.CharField(read_only=True)
    paid=serializers.CharField(read_only=True)
    amount_cents=serializers.CharField(read_only=True)
    currency=serializers.CharField(read_only=True)
    class Meta:
        model = PaymobOrder
        fields = "__all__"
