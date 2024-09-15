from django import forms
from .models import UploadModelConfig

class DatasetForm(forms.ModelForm):
    class Meta:
        model = UploadModelConfig
        fields = ['name', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
