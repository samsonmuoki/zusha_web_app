from django.db import models

# Create your models here.

APPROVED = 'approved'
BLACKLISTED = 'blacklisted'

STATUS = [
    (APPROVED, ('Approved to operate')),
    (BLACKLISTED, ('Not approved to operate')),
]


class Sacco(models.Model):
    """Sacco details."""

    sacco_name = models.CharField(max_length=200)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    license_status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return f"{self.sacco_name} => {self.license_status}"


class Vehicle(models.Model):
    """Vehicle details."""
    registration_number = models.CharField(max_length=200)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    license_status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return f"{self.registration_number} => {self.sacco}"


class Driver(models.Model):
    """Driver details."""

    driver_name = models.CharField(max_length=200)
    driver_id = models.CharField(max_length=200)
    # driver_id = models.IntegerField(default=0)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    license_status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return f"{self.driver_name} => {self.sacco}"
