from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

from .filters import HotelFilter, HotelChainFilter
from .models import Hotel, HotelChain, HotelDraft
from .serializers import HotelSerializer, HotelChainSerializer, HotelDraftSerializer
from .permissions import IsStaffUserOrReadOnly


class HotelChainViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUserOrReadOnly]
    queryset = HotelChain.objects.all().order_by("title")
    serializer_class = HotelChainSerializer
    lookup_field = "slug"
    filterset_class = HotelChainFilter


class HotelViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUserOrReadOnly]
    queryset = Hotel.objects.all().order_by("-created_at")
    serializer_class = HotelSerializer
    lookup_field = "slug"
    filterset_class = HotelFilter


class HotelDraftViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = HotelDraft.objects.all().order_by("-created_at")
    serializer_class = HotelDraftSerializer
    lookup_field = "slug"
