from multiprocessing.reduction import register

from rest_framework import permissions
from rest_framework.permissions import BasePermission





class OwnerProductUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.store_product.owner == request.user


class OwnerStoreUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class OrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            return True





