from .models import Hotel, HotelChain
from django_filters import rest_framework as filters


class HotelChainFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = HotelChain
        fields = ("name",)


class HotelFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    location = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Hotel
        fields = ("name", "location")
