from django import forms
from .models import ModelConfig

class DatasetForm(forms.ModelForm):
    class Meta:
        model = ModelConfig
        fields = ['name', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
