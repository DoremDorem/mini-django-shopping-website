from django.contrib import admin
from .models import Category
from django.utils.html import format_html
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=('cat_img','category_name')
    prepopulated_fields = {
        "slug": ("category_name",)
    }
    def cat_img(self,obj):
        if obj.cat_image:
            return format_html(
            '<img src="{}" width="45" height="45" style="object-fit:cover;border-radius:50%" />',
            obj.cat_image.url
            )
        return "no image"

admin.site.register(Category,CategoryAdmin)