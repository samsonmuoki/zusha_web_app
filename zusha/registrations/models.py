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
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return self.sacco_name


class Vehicle(models.Model):
    """This model stores details of all vehicles registered by NTSA."""
    registration_number = models.CharField(max_length=7, unique=True)
    # sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
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
    """Details of drivers registered to operate by NTSA"""

    driver_id = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=10)
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SaccoVehicle(models.Model):
    """Each sacco stores the details of the vehicles
    they operate in this model."""
    vehicle = models.OneToOneField(Vehicle, on_delete=models.PROTECT)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.vehicle}: {self.sacco}"


class SaccoDriver(models.Model):
    """Each sacco stores the details of drivers it has employed
    in this model."""
    driver = models.OneToOneField(Driver, on_delete=models.PROTECT)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.driver}: {self.sacco}"
