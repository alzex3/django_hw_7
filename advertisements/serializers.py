from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления"""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user

        user_open_advertisements = Advertisement.objects.filter(
            creator=validated_data["creator"]
        ).filter(status="OPEN").count()

        if user_open_advertisements < 10:
            return super().create(validated_data)
        else:
            raise serializers.ValidationError('Open advertisements limit exceeded!')

    def update(self, instance, validated_data):
        validated_data["creator"] = self.context["request"].user

        if validated_data["status"] == "OPEN":

            user_open_advertisements = Advertisement.objects.filter(
                creator=validated_data["creator"]
            ).filter(status="OPEN").count()

            if user_open_advertisements < 10:
                return super().update(instance, validated_data)
            else:
                raise serializers.ValidationError('Open advertisements limit exceeded!')

        return super().update(instance, validated_data)
