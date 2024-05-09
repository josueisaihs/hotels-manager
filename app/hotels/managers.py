from typing import Any
from django.db import models
from django.db.models import Q, F
from django.apps import apps

from functools import reduce

HotelModel = lambda: apps.get_model("hotels", "Hotel")
HotelChainModel = lambda: apps.get_model("hotels", "HotelChain")


class HotelChainManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        if "title" in kwargs:
            query = self.filter(title__iexact=kwargs["title"])
            if query.exists():
                return query.first()
            kwargs["title"] = kwargs["title"].title()

        return super().create(**kwargs)

    def filter_by_title_with_auto_assign(self, name: str) -> Any:
        """
        A function to get the chain by title with auto assign and more than 3 characters

        return: the chains if it exists, None otherwise
        """
        name_vector = name.lower().split(" ")
        query = (
            reduce(
                lambda x, y: x | y, [Q(title__icontains=word) for word in name_vector]
            )
            & Q(title__gt=3)
            & Q(auto_assign=True)
        )
        return self.filter(query)


class AbstractHotelManager(models.Manager):
    def nested_create(self, **kwargs: Any) -> Any:
        if "chain" in kwargs:
            chain = kwargs.pop("chain")
            if isinstance(chain, dict):
                chain = HotelChainModel().objects.create(**chain)
            kwargs["chain"] = chain

        return self.create(**kwargs)

    def nested_update(self, instance: Any, validated_data: Any) -> None:
        # No implemented yet
        chain_data = validated_data.pop("chain", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if chain_data:
            chain = instance.chain if instance.chain else HotelChainModel()
            for key, value in chain_data.items():
                setattr(chain, key, value)
            chain.save()  # type: ignore
            instance.chain = chain
        instance.save()
        return instance
