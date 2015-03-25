"""
These are sample tests for the sample application.
"""

from models import Company, NonForProfit, CEO
from django import test
import unittest
from django_webtest import DjangoTestApp, WebTest

class InheritTest(test.TestCase):
    """Test value inheritance of 'address' field of 'Company' model."""

    def setUp(self):
        self.ceo = CEO.objects.create(name='John')
        self.ceo2 = CEO.objects.create(name='Bill')

    def instance(self, **kwargs):
        """Return a fresh unsaved model instance."""
        return Company.objects.create(**kwargs)

    def test_orphan(self):
        """Company has no parents and has city set."""

        c = self.instance(name='company', city='NY', ceo=self.ceo)

        self.assertEqual(c.name, 'company')
        self.assertEqual(c.city, 'NY')
        self.assertEqual(c.ceo, self.ceo)

    def test_orphan_empty(self):
        """Now, it is empty."""

        c = self.instance(name='company')

        self.assertEqual(c.name, 'company')
        self.assertEqual(c.city, '')
        self.assertEqual(c.ceo, None)

    def test_inherit(self):
        """A child inherits value from a parent."""

        parent = self.instance(name='parent', city='NY', ceo=self.ceo)
        child = self.instance(parent=parent, name='child')
        child._inherit()

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.city, 'NY')
        self.assertEqual(child.ceo, self.ceo)

    def test_override(self):
        """A child overrides the value got from parent."""

        parent = self.instance(name='parent', city='NY', ceo=self.ceo)
        child = self.instance(parent=parent, name='child', city='SPB', ceo=self.ceo2)
        child._inherit()

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.city, 'SPB')
        self.assertEqual(child.ceo, self.ceo2)

    def test_manager(self):
        parent = self.instance(name='parent', city='NY', ceo=self.ceo)
        child = self.instance(parent=parent, name='child')

        child_inherited = child.__class__.objects.get_inherited(
            id=child.id
        )

        self.assertEqual(child_inherited.city, 'NY')

class InheritableChildModelTest(InheritTest):
    """An child (inherited) model is also inheritable."""

    def instance(self, **kwargs):
        return NonForProfit.objects.create(**kwargs)


class SaveTest(InheritTest):
    """Parent field."""

    def instance(self, **kwargs):
        return Company.objects.create(**kwargs)

    def test_save_inherit_none(self):
        parent = self.instance(name='parent', city='NY', ceo=self.ceo)
        child = self.instance(parent=parent, name='child')
        child._inherit() # Now city = 'NY'

        child.save() # We do not modify it and save

        self.assertEqual(
            Company.objects.get(name='child').city,
            ''
        ) # City should be None

    def test_save_override(self):
        parent = self.instance(name='parent', city='NY', ceo=self.ceo)
        child = self.instance(parent=parent, name='child')
        child._inherit() # Now city = 'NY'

        child.city = 'SPB'
        child.save() # Modified

        self.assertEqual(
            Company.objects.get(name='child').city,
            'SPB'
        ) # City should be None


class AdminTest(WebTest):
    fixtures = ('test_data.json', )

    app_class = DjangoTestApp
    csrf_checks = False

    def change_form(self, pk):
        return self.app.get(
            '/admin/sampleapp/company/%s/' % pk,
            user='admin'
        ).form

    def __test_disabled_fields(self):
        """Inherited fields are disabled."""

        Company.objects.filter(pk=2).update(
            ceo=None,
            address='',
            description=''
        )

        form = self.change_form(2)

        # ceo, address, and description are inherited. name is not.
        inherited_fields = ('ceo', 'address', 'description')
        overridden_fields = ('country', )

        for field in inherited_fields:
            value = form['%s_override' % field].value

            self.assertEqual(
                value, None,
                'Field %s seems to have "override" %s' % (field, value)
            )
            self.assertTrue(
                form.fields[field][0].attrs.get('disabled', False),
                'Field %s does not seem to be disabled' % field
            )

        for field in overridden_fields:
            self.assertEqual(
                form['%s_override' % field].value, 'on',
                'Field %s seems to have "override" off' % field
            )
            self.assertTrue(not form.fields[field][0].attrs.get('disabled', False))

