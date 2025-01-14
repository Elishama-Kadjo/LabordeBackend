from django.contrib import admin
from .models import CustomUser, UserResetPassword

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", 'email', 'first_name', 'last_name', 'is_staff', 'is_active', "is_superuser",]
    
@admin.register(UserResetPassword)
class UserResetPasswordAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "active", "expires_at"]