from django.conf import settings
from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'last_name',
        'first_name',
        'email',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE
