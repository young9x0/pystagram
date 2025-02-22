from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class FollowersInline(admin.TabularInline):
    model = User.following.through
    fk_name = "from_user"
    verbose_name = "the user I follow"
    verbose_name_plural = f"{verbose_name} list"
    extra = 1


class FollowingInline(admin.TabularInline):
    model = User.following.through
    fk_name = "to_user"
    verbose_name = "the user following me"
    verbose_name_plural = f"{verbose_name} list"
    extra = 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        ('private info', {"fields": ("first_name", "last_name", "email")}),
        ('add field', {"fields": ("profile_image", "short_description")}),
        ('authorization', {"fields": ("is_active", "is_staff", "is_superuser")}),
        ('important schedule', {"fields": ("last_login", "date_joined")}),
        ('related object', {"fields": ("like_posts",)}),
    ]

    inlines = [
        FollowersInline,
        FollowingInline,
    ]
