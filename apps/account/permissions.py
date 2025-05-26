from rest_framework import permissions
from .models import CustomUser

class OnlyProspectCanPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        is_prospect=CustomUser.objects.filter(id=request.user.id, status=CustomUser.EmployeeStatus.PROSPECT).exists()
        return is_prospect

class OnlyAttornyCanPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        is_attorny=CustomUser.objects.filter(id=request.user.id, status=CustomUser.EmployeeStatus.ATTORNEY).exists()
        return is_attorny


    