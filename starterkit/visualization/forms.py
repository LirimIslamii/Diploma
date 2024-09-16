from django import forms
from .models import ModelTrainingRecord

class ModelTrainingRecordForm(forms.ModelForm):
    class Meta:
        model = ModelTrainingRecord
        fields = [
            'dataset_name', 'model_name', 'description', 'is_active',
            'val_loss', 'val_accuracy', 'training_loss', 'training_accuracy',
            'precision', 'recall', 'f1_score', 'learning_rate', 'batch_size',
            'num_epochs', 'optimizer', 'loss_curve_url', 'accuracy_curve_url',
            'roc_curve_url'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'dataset_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Add more widgets as needed for better form control
        }
        labels = {
            'val_loss': 'Validation Loss',
            'val_accuracy': 'Validation Accuracy',
            # Add more labels as needed
        }
        help_texts = {
            'dataset_name': 'Enter the name of the dataset used.',
            # Add more help texts as needed
        }
