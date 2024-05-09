from rest_framework import serializers

from app.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes users
    """

    class Meta:
        model = User
        fields = [
            "email",
        ]
        read_only_fields = [
            "email",
        ]
