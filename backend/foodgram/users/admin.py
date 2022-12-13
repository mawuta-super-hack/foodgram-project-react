from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'author_id',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
