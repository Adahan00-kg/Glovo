from rest_framework import permissions





class OwnerProductUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.store_product.owner == request.user: # obj.store_product.adahan == request.adahan
            return True


class OwnerStoreUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True


class OrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.cart.product.store_product.owner:
            return True
        return False


class CheckOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'владелец магазина':
            return True


class CheckCourier(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'курьер':
            return False
        return True

class OwnerReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'владелец магазина' :
            return False
        elif request.user.role == 'курьер':
            return False
        else:
            return True


class ComboOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.product.store_product.owner :
            return True


class CheckReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class CheckClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        elif request.user == obj.cart.product.store_product.owner:
            return True
        return False


class CourierCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'курьер':
            return True
        return False
