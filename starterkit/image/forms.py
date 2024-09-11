from django import forms
from .models import ModelConfig

class ModelConfigForm(forms.ModelForm):
    class Meta:
        model = ModelConfig
        exclude = ('inserted_date','is_active')
