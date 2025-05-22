from django_filters import rest_framework as filters
from .models import CustomUser

class StaffFilter(filters.FilterSet):
    first_name=filters.CharFilter(lookup_expr='icontains')
    last_name=filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model=CustomUser
        fields=['status',]
