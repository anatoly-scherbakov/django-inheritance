from models import Company
from inheritance.admin import InheritanceAdmin
from django.contrib.admin import site


class CompanyAdmin(InheritanceAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'parent')}),
        ('Location', {'fields': ('address', 'address2', 'city', 'state', 'zipcode', 'country')}),
        ('About', {'fields': ('description', )}),
    )

site.register(Company, CompanyAdmin)