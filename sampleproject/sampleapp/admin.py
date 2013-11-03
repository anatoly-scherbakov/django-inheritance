from models import Company, CEO
from inheritance.admin import InheritanceAdmin
from django.contrib.admin import site, ModelAdmin

class CompanyAdmin(InheritanceAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'parent', 'ceo')}),
        ('Location', {'fields': ('address', 'address2', 'city', 'state', 'zipcode', 'country')}),
        ('About', {'fields': ('description', )}),
    )

class CeoAdmin(ModelAdmin):
    pass

site.register(Company, CompanyAdmin)
site.register(CEO, CeoAdmin)