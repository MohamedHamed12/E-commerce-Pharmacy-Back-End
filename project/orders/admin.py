# -*- coding: utf-8 -*-
from django.contrib import admin
from orders.models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
