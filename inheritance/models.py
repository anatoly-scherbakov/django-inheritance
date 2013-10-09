"""Generic models."""

from dirtyfields import DirtyFieldsMixin
from mptt.models import MPTTModel
from django.core.exceptions import ImproperlyConfigured


class Inheritable(MPTTModel, DirtyFieldsMixin):
    """
    Enables a Django model within an MPTT hierarchy to inherit field values from parent models.
    """

    @property
    def parent(self):
        raise NotImplementedError("The model should define a 'parent' field of type TreeForeignKey.")

    def _apply_inheritance(self):
        """Update inheritable field values from the DB.

        If a field is empty and there is a parent node, we fetch the field value from
        the parent.

        This way, we recurse through the whole tree."""

        self._inherited_fields = set()
        fields = getattr(self, 'inherit_fields', None)
        if fields and self.parent: # If there are inheritable fields and a parent node to inherit from
            for field in fields:
                value = getattr(self, field)

                # This node's own value is empty.
                if not value:
                    self._inherited_fields.add(field) # This field is now inherited
                    setattr(self, field, getattr(self.parent, field)) # And fetched from the parent

        # Reset dirty fields state
        self._reset_state()

    def __init__(self, *args, **kwargs):
        """Startup checks and caching."""

        if not isinstance(self, MPTTModel):
            raise ImproperlyConfigured("%s model is meant to support inheritance, but does not use django-mptt." % self)

        super(Inheritable, self).__init__(*args, **kwargs)

        self._apply_inheritance()

    def _as_dict(self):
        """
        This is a fix for DirtyFields app. DirtyFieldsMixin._as_dict() returns the fields
        which are local to the model, but not those which are inherited from parent models.
        Here, we fix it. See also: https://github.com/smn/django-dirtyfields/pull/3
        """
        return dict([(f.name, getattr(self, f.name)) for f in self._meta.fields if not f.rel])

    def save(self, *args, **kwargs):
        """If an inheritable field is:
            - actually inherited,
            - not changed by the user,
        it should be set to None."""

        # The fields that must be set to None include inherited fields, but not
        # dirty fields.

        fields_to_null = self._inherited_fields - \
                         set(self.get_dirty_fields().keys())

        for field in fields_to_null:
            setattr(self, field, None)

        super(Inheritable, self).save(*args, **kwargs)

        # Reapply inheritance logic to this model
        self._apply_inheritance()

    class Meta:
        abstract = True
        ordering = ('tree_id', 'lft')