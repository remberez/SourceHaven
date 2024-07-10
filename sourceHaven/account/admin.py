from django.contrib import admin
from .models import Profile, Contact


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('profile_name',)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
