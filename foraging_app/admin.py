from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.admin import SimpleListFilter
# from django.contrib.auth.admin import UserAdmin
from foraging_app.models.user import User, UserProfile

admin.site.register(User, UserProfile)

