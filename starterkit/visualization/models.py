from django.db import models

class ModelTrainingRecord(models.Model):
    dataset_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Update timestamp on model updates
    val_loss = models.FloatField()
    val_accuracy = models.FloatField()
    
    # Additional performance metrics
    training_loss = models.FloatField(default=0.0)
    training_accuracy = models.FloatField(default=0.0)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    
    # Hyperparameters for reproducibility
    learning_rate = models.FloatField(default=0.001)
    batch_size = models.IntegerField(default=32)
    num_epochs = models.IntegerField(default=10)
    optimizer = models.CharField(max_length=50, default='Adam')
    
    # URLs to stored graphs for visualization
    loss_curve_url = models.URLField(blank=True, null=True)
    accuracy_curve_url = models.URLField(blank=True, null=True)
    roc_curve_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'model_training_records'  # Ensure this matches the actual table name in SQL Server

    def __str__(self):
        return f"{self.model_name} on {self.dataset_name} - Active: {self.is_active}"
