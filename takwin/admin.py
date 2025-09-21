from django.contrib import admin
from .models import Takwin, UserTakwin

#, UserTakwin

@admin.register(Takwin)
class TakwinAdmin(admin.ModelAdmin):
    list_display = ("title", "aspect", "link")
    list_filter = ("aspect",)
    search_fields = ("title", "description")


admin.site.register(UserTakwin)



# @admin.register(UserTakwin)
# class UserTakwinAdmin(admin.ModelAdmin):
#     list_display = ("user", "takwin", "is_done")
#     list_filter = ("is_done", "takwin__aspect")
#     search_fields = ("user__email", "takwin__title")
