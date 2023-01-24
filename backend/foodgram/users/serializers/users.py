from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User


class UserCreateSerializer(UserCreateSerializer):
    """Cериализатор djoser для создания пользователя"""
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserListSerializer(UserSerializer):
    """Cериализатор djoser для управления пользователем"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """ Определение подписки пользователя на автора """
        user = self.context.get('request').user
        if user.is_anonymous or obj.username == user:
            return False
        return obj.follower.filter(user=obj, following=user).exists()
