from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import SimpleListFilter
from foraging_app.models.user import User

class BadgeFilter(SimpleListFilter):
    title = 'badge'
    parameter_name = 'badge'

    def lookups(self, request, model_admin):
        return User.BADGE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(badge=self.value())
        return queryset

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'rating', 'badge', 'created_since')
    list_filter = ('rating', BadgeFilter)  # Ensure this is a tuple
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('rating', 'badge', 'profile_image', 'created_since')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'rating', 'badge', 'profile_image', 'created_since'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

