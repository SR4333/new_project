from turtle import mode
from django.contrib import admin
from .models import book,Country

# Register your models here.
admin.site.register(book)
class CountryAdmin(admin.ModelAdmin):
    class Meta:
        model=Country
        list_display="__all__"
admin.site.register(Country,CountryAdmin)