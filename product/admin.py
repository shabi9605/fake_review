from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','description','slug']



admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductAdd)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Report)