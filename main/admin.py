from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Ads, Quotes, Suggestions

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "phone", "role", "education_level", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "role", "education_level")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("المعلومات الشخصية", {"fields": ("first_name", "last_name", "phone", "role", "education_level")}),
        ("الصلاحيات", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "phone", "role", "education_level", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'place', 'day')  # الحقول اللي تظهر في القائمة
    search_fields = ('title', 'place')  # البحث حسب العنوان أو المكان



admin.site.register(Quotes)
admin.site.register(Suggestions)