from django.contrib import admin
from inheritance.forms import InheritableForm
import models

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    form = InheritableForm

    fieldsets = (
        (None, {'fields': ('name', 'parent', 'ceo')}),
        ('Location', {'fields': ('address', 'address2', 'city', 'state', 'zipcode', 'country')}),
        ('About', {'fields': ('description', )}),
    )

admin.site.register(models.CEO)