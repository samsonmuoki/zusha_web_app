from django.db import models

# Create your models here.


class Sacco(models.Model):
    """Sacco details."""

    sacco_name = models.CharField(max_length=200)

    def __str__(self):
        return self.sacco_name


class Vehicle(models.Model):
    """Vehicle details."""
    registration_number = models.CharField(max_length=200)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.registration_number} => {self.sacco}"


class Driver(models.Model):
    """Driver details."""

    driver_name = models.CharField(max_length=200)
    driver_id = models.CharField(max_length=200)
    # driver_id = models.IntegerField(default=0)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.driver_name} => {self.sacco}"
