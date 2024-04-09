from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Family

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        ("정보", {"fields": ("first_name", "last_name", "email", "phone_number", "birth")}),
        ("가족", {"fields": ("family_id", "is_senior", "role")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("일정", {"fields": ("last_login", "date_joined")}),
    ]

class UserInLine(admin.TabularInline):
    model = User
    extra = 0

    fieldsets = [
        (None, {"fields": ["username", "role", "first_name", "last_name"]})
    ]

class FamilyAdmin(admin.ModelAdmin):
    list_display = ["id", "family_name"]
    inlines = [
        UserInLine,
    ]
    fieldsets = [
        (None, {"fields": ("family_name",)}),
        ("정보", {"fields": ("senior_id", "senior_birth", "senior_gender", "senior_diseases", "senior_interests")}),
        ("루틴", {"fields": ("morning", "evening", "breakfast", "lunch", "dinner")}),
    ]
    

admin.site.register(Family, FamilyAdmin)