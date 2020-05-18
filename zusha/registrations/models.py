from django.db import models

# Create your models here.

APPROVED = 'approved'
BLACKLISTED = 'blacklisted'
EXPIRED = 'expired'

LICENSE_STATUS = [
    (APPROVED, ('Approved to operate')),
    (EXPIRED, ('License not renewed')),
    (BLACKLISTED, ('Not approved to operate')),
]


class Sacco(models.Model):
    """Sacco details."""

    sacco_name = models.CharField(max_length=200, primary_key=True)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return self.sacco_name


class Vehicle(models.Model):
    """Vehicle details."""
    registration_number = models.CharField(max_length=200)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return self.registration_number


class Driver(models.Model):
    """Driver details."""

    driver_id = models.CharField(max_length=200)
    driver_name = models.CharField(max_length=200)
    # driver_id = models.IntegerField(default=0)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    # sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return self.driver_name
