django-inheritance
==================

An implementation of prototypal inheritance for Django model instances.

Motivation
----------

Prototypal inheritance can be a very handy concept for some subject areas. For example, you have got a `Company` model with a hierarchy defined (any company can have several subsidiaries). It is often the case that subsidiaries inherit lots of field values from parents, for example -- city or juridical type. `django-inheritance` allows to mark model fields inheritable. Imagine that `Company` model has `city` field which is inheritable. Then:

```python
>>> parent = Company.objects.create(city='NY')
>>> child  = Company.objects.create(parent=parent)
>>> child.city
'NY'
```

As `child.city` is empty, it inherits value from parent object.

Usage
-----

Requirements:

* django-mptt
* django-dirtyfields

Both of them can be installed by `pip`.

* Copy `inheritance` folder somewhere at your Python path
* Add `'inheritance'` to `INSTALLED_APPS`
* Inherit the necessary model from `inheritance.models.Inheritable`
* To establish a hierarchy on this model, add a `parent` field of type `mptt.TreeForeignKey`.
* Add `inherit_fields` attribute. It must be a tuple of names of fields which must be inherited. Note that these fields must have `blank=True` and `null=True`.
* You can inherit your model admin class from `inheritance.admin.InheritanceAdmin` to enable a nice form with checkboxes in Django admin panel.

You can see a working Django example project at `sampleproject` directory. Just run `./manage.py runserver` there. Run `./manage.py test sampleapp` to test how it works if you make any changes to the code.

Status
------

This app is being actively developed and used in a production system. But is it yet in alpha stage because many features are not implemented/tested. Known problems:

* The application is not tested with any field types besides `CharField` and `TextField`.
* You cannot use an empty value without inheriting parent value.
* In model admin class, you must specify the `fieldsets` property.
* There is no support for model forms (besides those in admin section).

Acknowledgements
----------------

This app development is funded by Vboost Inc., http://vboost.com. Released to Open Source with permission. You can use, modify, and redistribute it under the terms of MIT software license.