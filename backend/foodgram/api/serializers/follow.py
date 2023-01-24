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
    recipes = FollowRecipeSerializers(many=True)
    recipes_count = serializers.IntegerField(
        source='author.recipes.count', read_only=True
    )

    class Meta:
        model = Follow
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

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        if Follow.objects.filter(user=user, author=instance.author):
            return True
        return False


    def get_recipes(self, instance):
        recipes = instance.author.recipe.all()
        return FollowRecipeSerializers(recipes, many=True).data