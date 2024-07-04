# -*- coding: utf-8 -*-
# permissions.py
from rest_framework.permissions import SAFE_METHODS, BasePermission


class SafePermission(BasePermission):
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) and staff users
        if (request.method in SAFE_METHODS) or request.user.is_staff:
            return True
        return False


class WishlistPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return  request.user.is_staff or request.user==obj.user
