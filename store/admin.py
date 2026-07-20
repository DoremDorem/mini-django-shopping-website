from django.contrib import admin
from django.utils.html import format_html
from .models import Product,Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={
        'slug':("product_name",)
    }

    # Right-side filters
    list_filter = (
        "is_available",
        "created_date",
        "modified_date",
    )

    # Default ordering
    ordering = (
        "-created_date",
    )

    # Number of products per page
    list_per_page = 20
     # Stock status


    readonly_fields = (
        "created_date",
        "modified_date",
    )

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "product_name",
                    "slug",
                    "description",
                    "product_detail",
                    "modal",
                    "category"
                )
            }
        ),

        (
            "Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "stock",
                    "is_available",
                )
            }
        ),

        (
            "Product Information",
            {
                "fields": (
                    "created_date",
                    "modified_date",
                ),
                "classes": (
                    "collapse",
                ),
            }
        ),
    )

    def product_image(self, obj):
        if obj.images:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover; border-radius:8px;" />',
                obj.images.url
            )

        return "No Image"


    @admin.display(description="Stock Status")
    def stock_status(self, obj):
        if obj.stock == 0:
            return "Out of Stock"

        elif obj.stock < 10:
            return "Low Stock"

        return "In Stock"
    
    list_display=('product_image','product_name','price','stock','is_available','created_date','modified_date')

class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value')


admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)