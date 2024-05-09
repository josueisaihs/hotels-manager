from django.forms import model_to_dict
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Hotel, HotelChain, HotelDraft

User = get_user_model()


class HotelChainSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes hotel chains
    """

    price_tag = SerializerMethodField()
    number_of_hotels = SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="hotelchain-detail", lookup_field="slug"
    )

    def get_price_tag(self, obj):
        return obj.price_tag

    def get_number_of_hotels(self, obj):
        return obj.number_of_hotels

    class Meta:
        model = HotelChain
        fields = "__all__"


class HotelSerializer(serializers.ModelSerializer):
    """
    Serializes hotels
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="hotel-detail", lookup_field="slug"
    )
    chain = HotelChainSerializer()
    related_hotels = SerializerMethodField()

    class Meta:
        model = Hotel
        fields = "__all__"

    def get_related_hotels(self, obj):
        return obj.related_hotels.values_list("pk", flat=True)

    def create(self, validated_data) -> Hotel:
        return Hotel.objects.nested_create(**validated_data)  # type: ignore

    def update(self, instance: Hotel, validated_data) -> Hotel:
        chain_data = validated_data.pop("chain", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if chain_data:
            chain = instance.chain if instance.chain else HotelChain()
            for key, value in chain_data.items():
                setattr(chain, key, value)
            chain.save()  # type: ignore
            instance.chain = chain
        instance.save()
        return instance


class HotelDraftSerializer(serializers.ModelSerializer):
    """
    Serializes hotel drafts
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="hoteldraft-detail", lookup_field="slug"
    )
    hotel = serializers.SlugRelatedField(
        queryset=Hotel.objects.all(), slug_field="slug"
    )
    chain = HotelChainSerializer()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HotelDraft
        fields = "__all__"
        read_only_fields = ("status",)

    def _assign_user(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return validated_data

    def create(self, validated_data) -> HotelDraft:
        return HotelDraft.objects.nested_create(**self._assign_user(validated_data))  # type: ignore

    def update(self, instance: HotelDraft, validated_data) -> HotelDraft:
        validated_data = self._assign_user(validated_data)

        chain_data = validated_data.pop("chain", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if chain_data:
            chain = instance.chain if instance.chain else HotelChain()
            for key, value in chain_data.items():
                setattr(chain, key, value)
            chain.save()  # type: ignore
            instance.chain = chain
        instance.save()
        return instance
