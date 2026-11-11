
from django import forms
from .models import Appliance, RepairRecord

class ApplianceForm(forms.ModelForm):

    class Meta:
        model = Appliance
        exclude = ['owner', 'created_at']

        widgets = {
            'purchase_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'notes': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

class RepairForm(forms.ModelForm):

    class Meta:
        model = RepairRecord
        fields = [
            'appliance',
            'issue',
            'service_center',
            'repair_date',
            'repair_cost',
            'status',
        ]

        widgets = {
            'repair_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'issue': forms.Textarea(
                attrs={'rows': 3}
            ),
        }