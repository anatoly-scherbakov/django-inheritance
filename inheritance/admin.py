"""Generic admin classes."""

from django.contrib.admin import ModelAdmin
from django.core.exceptions import ImproperlyConfigured
from copy import deepcopy
from forms import InheritanceForm
from mptt.admin import MPTTModelAdmin

class InheritanceAdmin(ModelAdmin):
    change_form_template = "inheritance/change_form.html"
    form = InheritanceForm

    def __init__(self, model, admin_site):
        super(InheritanceAdmin, self).__init__(model, admin_site)

        self.exclude = self.exclude or []

        for field in model.inherit_fields:
            self.exclude.append('%s_override' % field)

    def get_fieldsets(self, request, obj=None):
        """Hook for specifying fieldsets for the add form.

        We add _override checkboxes for the fields that need them.

        See related Django bug: https://code.djangoproject.com/ticket/12238"""

        # This row was worth several days of torments. It is VERY important
        # because, if removed, multiple *_override fields appear in the fieldset
        # and ugly bugs occur in the deepness of Django magic.

        if not getattr(self, 'fieldsets', None):
            raise ImproperlyConfigured("Admin class for model %s must have 'fieldsets' attribute defined." % type(obj))

        fieldsets = deepcopy(self.fieldsets)

        for name, options in fieldsets:
            fields = options['fields']
            over   = []
            
            for field in fields:
                if field in self.model.inherit_fields:
                    over.append('%s_override' % field)
                over.append(field)

            options['fields'] = over

        return fieldsets

    class Media:
        js = ('/static/inheritance/inheritance-admin.js', )
        css = {
            'all': ('/static/inheritance/inheritance-admin.css', ),
        }
