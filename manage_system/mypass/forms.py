# mypass/forms.py
from django import forms
from .models import GatePass

class ReturnableGatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = [
            'pass_id', 'institution_department', 'sub_department',
            'material_product_name', 'material_product_quantity', 'product_material_serial_number', 
            'product_material_description', 'product_image', 'reason', 'expected_return_date', 
            'employee_name', 'employee_id', 'designation', 'department', 'contact_info'
        ]
        widgets = {
            'expected_return_date': forms.DateInput(attrs={'type': 'date'}),
        }

class NonReturnableGatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = [
            'pass_id', 'institution_department', 'sub_department',
            'material_product_name', 'material_product_quantity', 'product_material_serial_number', 
            'product_material_description', 'product_image', 'reason', 
            'employee_name', 'employee_id', 'designation', 'department', 'contact_info'
        ] 

