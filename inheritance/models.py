"""Generic models."""

from django.db import models
from django.db.models.query import QuerySet
from dirtyfields import DirtyFieldsMixin
from mptt.models import MPTTModel, TreeManager



class InheritanceQuerySet(QuerySet):
    def get_inherited(self, *args, **kwargs):
        """Get instance with inherited values."""
        instance = self.get(*args, **kwargs)
        instance._inherit()
        return instance


class InheritanceManager(TreeManager):
    """Inheritance manager."""

    def get_queryset(self):
        return InheritanceQuerySet(
            self.model, using=self._db
        ).order_by(
            self.tree_id_attr, self.left_attr
        )

    def get_inherited(self, *args, **kwargs):
        return self.get_queryset().get_inherited(*args, **kwargs)


class Inheritable(DirtyFieldsMixin, MPTTModel):
    """Base model, enables prototypal inheritance."""

    # Field values considered empty
    EMPTY_VALUES = ['', None]

    # Which fields are we going to inherit?
    inheritable_fields = None

    # Which fields are inherited in the current instance
    _inherited_fields = None

    # List of empty values
    _empty_fields = None

    objects = InheritanceManager()

    @property
    def parent(self):
        """Crying out loud."""
        raise NotImplementedError("`parent` TreeForeignKey field required.")

    def _inherit_field(self, field, ancestors):
        """Inherit a single field value."""
        self._empty_fields[field] = getattr(self, field)

        for depth, instance in enumerate(ancestors):
            value = getattr(instance, field)

            # Is the value empty?
            # We cannot just plain use "if value" because 0 is not an empty value, from our point of view,
            # but __bool__ thinks it coerces to False. So we maintain an explicit list.
            if value not in self.EMPTY_VALUES:
                # Found something

                if depth:
                    # It is inherited from a parent indeed
                    self._inherited_fields.add(field)  # Take a note
                    setattr(self, field, value)        # And make it available

                # We are done on that
                return value

    def _inherit(self):
        """Update inheritable field values from the DB.

        If a field is empty and there is a parent node, we fetch the field value from
        the parent.

        This way, we recurse through the whole tree."""

        self._empty_fields = {}
        self._inherited_fields = set()

        fields = getattr(self, 'inheritable_fields', None)
        ancestors = self.get_ancestors(ascending=True, include_self=True)

        if fields and self.parent_id: # If there are inheritable fields and a parent node to inherit from
            for field in fields:
                self._inherit_field(field, ancestors)

        # Reset DirtyFields state, to say that we haven't changed anything
        self._original_state = self._full_dict()

    def save(self, *args, **kwargs):
        """If an inheritable field is:
            - actually inherited,
            - not changed by the user,
        it should be set to None."""

        # The fields that must be set to None include inherited fields, but not
        # dirty fields.

        if self._inherited_fields:
            fields_to_empty = (self._inherited_fields or set()) - \
                             set(self.get_dirty_fields(check_relationship=True).keys())

            for field in fields_to_empty:
                setattr(
                    self, field,
                    self._empty_fields[field]
                )

            # Actually save it
            super(Inheritable, self).save(*args, **kwargs)

            # Reapply inheritance logic to this instance
            self._inherit()

        else:
            return super(Inheritable, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['tree_id', 'lft']


'''
class _Inheritable(MPTTModel, DirtyFieldsMixin):
    """
    Enables a Django model within an MPTT hierarchy to inherit field values from parent models.
    """

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
        values = {}
        for field in self._meta.fields:
            name = field.name
            try:
                value = getattr(self, name)
            except:
                value = None

            values[name] = value

        return values

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
'''

