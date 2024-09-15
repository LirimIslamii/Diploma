from django import forms
from .models import ParamsModelConfig

class ModelConfigForm(forms.ModelForm):
    class Meta:
        model = ParamsModelConfig  
        exclude = ('inserted_date','is_active')
