from django.contrib import admin
from .models import Committee, UserCommittee


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('title', 'committees', 'link')  # أعمدة تظهر في القائمة
    search_fields = ('title', 'description')        # البحث
    list_filter = ('committees', 'education_levels') # فلاتر جانبية
    ordering = ('title',)                           # الترتيب الافتراضي


@admin.register(UserCommittee)
class UserCommitteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'committee', 'is_added')
    list_filter = ('is_added', 'committee')
    search_fields = ('user__email', 'committee__title')
    ordering = ('user',)
