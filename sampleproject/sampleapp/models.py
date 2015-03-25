from django.db import models
from inheritance.models import Inheritable
from mptt.models import TreeForeignKey


class CEO(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'CEO'
        verbose_name_plural = 'CEOs'


class Company(Inheritable):
    """A company model with enabled inheritance."""

    # Companies form a hierarchy with django-mptt, where any company can have a number of subsidiaries.
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subsidiaries')

    # Not inheritable field
    name = models.CharField('Company name', max_length=100, unique=True)

    # Address data
    address = models.CharField('Address', max_length=100, blank=True)
    address2 = models.CharField('Address 2', max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField('Zip Code', max_length=11, blank=True)
    country = models.CharField(max_length=2, blank=True)

    # Etc
    description = models.TextField(blank=True)

    # Foreign field
    ceo = models.ForeignKey(CEO, blank=True, null=True)

    # List of fields with inheritable values
    inheritable_fields = [
        'address', 'address2', 'city', 'state', 'zipcode', 'country',
        'description', 'ceo'
    ]

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'

class NonForProfit(Company):
    """A model inherited from company."""

    notes = models.TextField(blank=True, null=True)