# -*- coding: utf-8 -*-
from products.permissions import SafePermission
from rest_framework import viewsets

from project.pharmacy.filters import PharmacyFilter
from project.products.pagination import ProductPagination

from .models import *
from .serializers import *


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [SafePermission]
    filterset_class = PharmacyFilter
    pagination_class = ProductPagination
