"""Generic forms."""

from django import forms


class InheritableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InheritableForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.parent:
            # Get parent of the current instance
            parent = self.instance.__class__.objects.get_inherited(
                id=self.instance.parent.pk
            )

            # Add placeholders
            for field in self.instance.inheritable_fields:
                self.fields[field].widget.attrs.update({
                    'placeholder': getattr(parent, field),
                })

    def ____init__(self, *args, **kwargs):
        """On init, the form adds "Override" checkboxes and sets their values."""

        super(InheritableForm, self).__init__(*args, **kwargs)

        # A checkbox must be added to every inheritable field.
        for field in self.instance.inherit_fields:
            if self.fields.get(field, None):
                is_overridden = field not in self.instance._inherited_fields
                override_name = '%s_override' % field
                
                checkbox = forms.BooleanField(
                    initial=is_overridden,
                    required=False,
                    label='Override',
                )

                # Adding checkbox
                self.fields[override_name] = checkbox

                # Mark field as inheritable
                self.fields[field].inheritable = True

                # Disable inherited fields
                if not is_overridden:
                    widget = self.fields[field].widget

                    # If this has got an inner widget, select it instead. Applies to RelatedAdminWidgetWrapper.
                    subwidget = getattr(widget, 'widget', None)
                    if subwidget:
                        widget.can_add_related = False
                        widget = subwidget

                    # Disable it
                    widget.attrs['disabled'] = 'disabled'

    def __save(self, *args, **kwargs):
        """Save form logic.

        In essence, the form should set not-overridden but inherited fields to None. Just it."""

        data = self.cleaned_data

        for field in self.instance.inherit_fields:
            if data.get(field, None) and not data.get('%s_override' % field, True):
                data[field] = ''

        return super(InheritableForm, self).save(*args, **kwargs)
        





