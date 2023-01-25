from django.contrib import admin
from .models import (
    User, File, News,
    Player, Trophy,
    Match, Sponsor,
    RoleHistory
)
from django.forms import TextInput, Textarea
from django.db import models


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'role', 'first_name')
    list_filter = ('email', 'first_name', 'role')
    list_display = ('email', 'role', 'first_name', 'last_name',
                    'is_superuser', 'is_active', 'is_staff')
    # prepopulated_fileds = {}


admin.site.register(File)
admin.site.register(News)
admin.site.register(Player)
admin.site.register(Trophy)
admin.site.register(RoleHistory)
admin.site.register(Match)
admin.site.register(Sponsor)
