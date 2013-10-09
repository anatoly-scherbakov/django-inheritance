"""Generic forms."""

from django import forms

class InheritanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """On init, the form adds "Override" checkboxes and sets their values."""

        super(InheritanceForm, self).__init__(*args, **kwargs)

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
                    self.fields[field].widget.attrs['disabled'] = True
    
    def save(self, *args, **kwargs):
        """Save form logic.

        In essence, the form should set not-overridden but inherited fields to None. Just it."""

        data = self.cleaned_data

        for field in self.instance.inherit_fields:
            if data.get(field, None) and not data.get('%s_override' % field, True):
                data[field] = ''

        return super(InheritanceForm, self).save(*args, **kwargs)
        





