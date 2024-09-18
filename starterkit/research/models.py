from django.db import models

class Image(models.Model):
    file_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    resolution = models.CharField(max_length=50)
    predicted_class = models.CharField(max_length=100)
    prediction_probabilities = models.TextField()
    image_data = models.BinaryField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name