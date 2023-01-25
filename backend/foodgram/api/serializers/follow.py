from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe
from users.models import Follow, User


class FollowCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания подписки/отписки на пользователя"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = (
            'user',
            'following',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя',
            )
        ]

    def validate_following(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя!"
            )
        return value


class FollowRecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowListSerializer(serializers.ModelSerializer):
    """ Сериализатор подписки и отписки на пользователя"""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipe_author.count', read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'is_subscribed',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        if user.is_anonymous or instance.username == user:
            return False
        return instance.follower.filter(user=instance, following=user).exists()

    def get_recipes(self, instance):
        recipes = instance.recipe_author.all()
        context = {'request': self.context.get('request')}
        return FollowRecipeSerializers(
            recipes,
            context=context,
            many=True
        ).data
