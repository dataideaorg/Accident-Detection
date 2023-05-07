from django.db import models

class Prediction(models.Model):
    prediction = models.CharField(max_length=255)
    confidence = models.FloatField()
    date = models.CharField(max_length=255, default="not_set")
    time = models.CharField(max_length=255, default='not_set')
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prediction} with {self.confidence}% confidence at {self.date,  self.time} in {self.location}"
