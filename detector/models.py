from django.db import models

class Prediction(models.Model):
    prediction = models.CharField(max_length=255)
    confidence = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prediction} with {self.confidence}% confidence at {self.date_time} in {self.location}"
