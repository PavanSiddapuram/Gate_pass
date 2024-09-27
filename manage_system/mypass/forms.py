from django import forms
from .models import GatePass

class ReturnableGatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = [
            'institution', 'sub_department', 'product_name',
            'product_quantity', 'product_serial_nos',
            'product_description', 'product_image', 'reason',
            'expected_return_date',  # Specific to returnable gate passes
            'employee_name', 'employee_id', 'designation',
            'contact_info'
        ]
        widgets = {
            'expected_return_date': forms.DateInput(attrs={'type': 'date'}),
            'product_image': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReturnableGatePassForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['employee_name'].initial = user.username  # Populating username as employee name
            self.fields['institution'].initial = user.userprofile.institution  # Assuming institution is in UserProfile
            self.fields['sub_department'].initial = user.userprofile.sub_department  # Assuming sub-department is in UserProfile


class NonReturnableGatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = [
            'institution', 'sub_department', 'product_name',
            'product_quantity', 'product_serial_nos',
            'product_description', 'product_image', 'reason',
            'employee_name', 'employee_id', 'designation',
            'contact_info'
        ]
        widgets = {
            'product_image': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NonReturnableGatePassForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['employee_name'].initial = user.username  # Populating username as employee name
            self.fields['institution'].initial = user.userprofile.institution  # Assuming institution is in UserProfile
            self.fields['sub_department'].initial = user.userprofile.sub_department  # Assuming sub-department is in UserProfile
