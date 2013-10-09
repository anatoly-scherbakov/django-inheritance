"""
These are sample tests for the sample application.
"""

from models import Company, NonForProfit
from django.test import TestCase


class UnsavedInheritanceTest(TestCase):
    """Test value inheritance of 'address' field of 'Company' model."""

    def instance(self, **kwargs):
        """Return a fresh unsaved model instance."""

        return Company(**kwargs)

    def test_orphan(self):
        """Company has no parents and has city set."""

        c = self.instance(name='company', city='NY')

        self.assertEqual(c.name, 'company')
        self.assertEqual(c.city, 'NY')

    def test_orphan_empty(self):
        """Now, it is empty."""

        c = self.instance(name='company')

        self.assertEqual(c.name, 'company')
        self.assertEqual(c.city, None)

    def test_inherit(self):
        """A child inherits value from a parent."""

        parent = self.instance(name='parent', city='NY')
        child = self.instance(parent=parent, name='child')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.city, 'NY')

    def test_override(self):
        """A child overrides the value got from parent."""

        parent = self.instance(name='parent', city='NY')
        child = self.instance(parent=parent, name='child', city='SPB')

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.city, 'SPB')


class UnsavedParentFieldInheritanceTest(UnsavedInheritanceTest):
    """Using the model field which is not local but inherited from another model class."""

    def instance(self, **kwargs):
        """Return a fresh unsaved model instance."""

        return NonForProfit(**kwargs)


class SavedInheritanceTest(UnsavedInheritanceTest):
    """Everything the same, but model instances are saved."""

    def instance(self, **kwargs):
        return Company.objects.create(**kwargs)


class SavedParentFieldInheritanceTest(SavedInheritanceTest):
    """Parent field."""

    def instance(self, **kwargs):
        return NonForProfit.objects.create(**kwargs)


class SavingInheritanceTest(UnsavedInheritanceTest):
    """Just as in previous cases, but the instance is being saved to the db."""

    def instance(self, **kwargs):
        instance = Company(**kwargs)
        instance.save()

        return instance

class SavingParentFieldInheritanceTest(SavingInheritanceTest):
    """Parent field."""

    def instance(self, **kwargs):
        instance = NonForProfit(**kwargs)
        instance.save()

        return instance
