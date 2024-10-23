from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'is_superuser']
    ordering = ['date_joined']
    search_fields = ['username', 'phone_number']

