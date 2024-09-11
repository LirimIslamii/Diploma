from django.db import models
from django.utils import timezone

class ModelConfig(models.Model):
    learning_rate = models.FloatField()
    num_epochs = models.IntegerField()
    kernel_size = models.CharField(max_length=10)
    optimizer = models.CharField(max_length=50)
    metrics = models.CharField(max_length=100)
    batch_size = models.IntegerField()
    num_kernels = models.IntegerField()
    early_stopping = models.BooleanField()
    validation_split = models.FloatField()
    lr_scheduler_params = models.TextField()
    is_active = models.BooleanField(default=True)
    inserted_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Config {self.id} - Optimizer: {self.optimizer}"
