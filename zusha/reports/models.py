from django.db import models


# Create your models here.


class Report(models.Model):
    """Store cases reported by passengers."""
    regno = models.CharField(max_length=10)
    sacco = models.CharField(max_length=10)
    speed = models.CharField(max_length=10)
    time = models.DateTimeField
    location = models.CharField(max_length=100)
    driver = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.regno} {self.speed}"
