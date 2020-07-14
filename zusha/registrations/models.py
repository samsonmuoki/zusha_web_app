import uuid
from django.db import models

# Create your models here.

APPROVED = 'Approved'
BLACKLISTED = 'Blacklisted'
EXPIRED = 'Expired'

LICENSE_STATUS = [
    (APPROVED, ('Approved to operate')),
    (EXPIRED, ('License not renewed')),
    (BLACKLISTED, ('Not approved to operate')),
]

LICENSE_CATEGORIES = [
    ('A', ('A')),
    ('B', ('B')),
    ('C', ('C')),
    ('D', ('D')),
    ('E', ('E')),
    ('F', ('F')),
    ('G', ('G')),
]

SACCO_DRIVER_STATUS = [
    ('Approved', ('Approved to operate')),
    ('Suspended', ('Suspended for the time being')),
    ('Blacklisted', ('Blacklisted from operating'))
]

VEHICLE_BODY_TYPES = [
    ('van', ('Van')),
    ('minivan', ('Minivan')),
    ('bus', ('Bus')),
    ('minibus', ('Minibus')),
    ('convertible', ('Convertible')),
    ('coupe', ('Coupe')),
    ('crossover', ('Crossover')),
    ('Hatchback', ('Hatchback')),
    ('luxury', ('Luxury')),
    ('muv', ('Multi-Utility Vehicle')),
    ('notchback', ('Notchback')),
    ('sedan', ('Sedan')),
    ('sportscar', ('Sports Car')),
    ('suv', ('Sports Utility Vehicle')),
    ('wagon', ('Wagon')),
    ('supercars', ('Super Cars')),
    ('truck', ('Truck')),
]

PUBLIC_TRANSPORT_VEHICLES = [
    'van',
    'minivan',
    'bus',
    'minibus',
]

GENDER_CHOICES = [
    ('male', ('Male')),
    ('female', ('Female')),
    ('other', ('Other')),
]

BLOOD_GROUPS = [
    ('A+', ('A+')),
    ('A-', ('A-')),
    ('B+', ('B+')),
    ('B-', ('B-')),
    ('O+', ('O+')),
    ('O-', ('O-')),
    ('AB', ('AB+')),
    ('AB', ('AB-')),
]

COUNTIES = [
    ("Mombasa", ("Mombasa")),
    ("Kwale", ("Kwale")),
    ("Kilifi", ("Kilifi")),
    ("Tana River", ("Tana River")),
    ("Lamu", ("Lamu")),
    ("Taita-Taveta", ("Taita/Taveta")),
    ("Garissa", ("Garissa")),
    ("Wajir", ("Wajir")),
    ("Mandera", ("Mandera")),
    ("Marsabit", ("Marsabit")),
    ("Isiolo", ("Isiolo")),
    ("Meru", ("Meru")),
    ("Tharaka-Nithi", ("Tharaka-Nithi")),
    ("Embu", "Embu"),
    ("Kitui", "Kitui"),
    ("Machakos", "Machakos"),
    ("Makueni", ("Makueni")),
    ("Nyandarua", ("Nyandarua")),
    ("Nyeri", ("Nyeri")),
    ("Kirinyaga", ("Kirinyaga")),
    ("Muranga", ("Murang'a")),
    ("Kiambu", ("Kiambu")),
    ("Turkana", "Turkana"),
    ("West Pokot", ("West Pokot")),
    ("Samburu", ("Samburu")),
    ("Trans Nzoia", ("Trans Nzoia")),
    ("Uasin Gishu", ("Uasin Gishu")),
    ("Elgeyo-Marakwet", ("Elgeyo/Marakwet")),
    ("Nandi", ("Nandi")),
    ("Baringo", ("Baringo")),
    ("Laikipia", ("Laikipia")),
    ("Nakuru", ("Nakuru")),
    ("Narok", ("Narok")),
    ("Kajiado", ("Kajiado")),
    ("Kericho", ("Kericho")),
    ("Bomet", ("Bomet")),
    ("Kakamega", ("Kakamega")),
    ("Vihiga", ("Vihiga")),
    ("Bungoma", ("Bungoma")),
    ("Busia", ("Busia")),
    ("Siaya", ("Siaya")),
    ("Kisumu", ("Kisumu")),
    ("Homa Bay", ("Homa Bay")),
    ("Migori", ("Migori")),
    ("Kisii", ("Kisii")),
    ("Nyamira", ("Nyamira")),
    ("Nairobi", ("Nairobi")),
]


class Vehicle(models.Model):
    """This model stores details of all vehicles registered by NTSA."""
    registration_number = models.CharField(max_length=7, unique=True)
    # date registered = models.DateField
    # last_report_revision_date = models.DateField
    name_of_owner = models.CharField(max_length=50)
    owner_national_id = models.CharField(max_length=10)
    year_of_manufacture = models.IntegerField()
    engine_capacity = models.IntegerField(null=False)
    vehicle_body_type = models.CharField(
        max_length=20,
        choices=VEHICLE_BODY_TYPES,
        null=False
    )
    color_of_vehicle = models.CharField(max_length=20)
    registered_logbook_number = models.CharField(max_length=50)
    registered_engine_number = models.CharField(max_length=50)
    registered_chasis_number = models.CharField(max_length=50)
    last_inspection_date = models.DateField(
        auto_now=False, auto_now_add=False
    )
    inspection_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )

    def __str__(self):
        return "{} {} {}".format(
            self.registration_number,
            self.vehicle_body_type,
            self.inspection_status
        )

    def is_for_public_transport(self):
        """Determine vehicles that are eligible for public transport."""
        if self.vehicle_body_type in PUBLIC_TRANSPORT_VEHICLES:
            return True

    def is_approved(self):
        """."""
        if self.inspection_status == APPROVED:
            return True


class RegisteredDriver(models.Model):
    """Details of drivers registered to operate by NTSA"""

    national_id = models.CharField(max_length=8, unique=True)
    surname = models.CharField(max_length=10)
    other_names = models.CharField(max_length=10)
    date_of_birth = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS)
    license_number = models.CharField(max_length=10)
    license_categories = models.CharField(
        max_length=50,
        choices=LICENSE_CATEGORIES
    )
    date_of_issue = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    date_of_expiry = models.DateField(
        auto_now_add=False,
        auto_now=False
    )
    county_of_residence = models.CharField(
        max_length=20,
        choices=COUNTIES
    )
    # date registered = models.DateField
    last_revision_date = models.DateField
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=10)
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )
    # license_status_logs = GenericField
    # license_renewal_logs = GenericField

    def __str__(self):
        return "{} {} {} {}".format(
            self.surname,
            self.other_names,
            self.license_number,
            self.license_status,
        )

    def name(self):
        """Driver full names."""
        return "{} {}".format(
            self.surname, self.other_names
        )

    def is_approved(self):
        if self.license_status == APPROVED:
            return True


class Sacco(models.Model):
    """Sacco details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    sacco_name = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)
    date_registered = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_inspection_date = models.DateField(auto_now_add=False, auto_now=False)
    license_status = models.CharField(
        max_length=32,
        choices=LICENSE_STATUS,
        default=APPROVED,
    )
    # license_status_logs = GenericField
    # license_renewal_logs = GenericField

    def __str__(self):
        return f"{self.sacco_name} -> {self.license_status}"


class SaccoVehicle(models.Model):
    """Sacco Vehicles list.

    Each sacco stores the details of the vehicles
    they operate in this model."""
    vehicle = models.OneToOneField(Vehicle, on_delete=models.PROTECT)
    date_registered = models.DateField(
        auto_now=False, auto_now_add=True
    )
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.vehicle}: {self.sacco}"


class SaccoDriver(models.Model):
    """Sacco Drivers list.

    Each sacco stores the details of drivers it has employed
    in this model."""
    driver = models.OneToOneField(RegisteredDriver, on_delete=models.PROTECT)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=SACCO_DRIVER_STATUS, default='Approved'
    )
    date_registered = models.DateField(
        auto_now=False, auto_now_add=True
    )
    last_status_update_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    description = models.TextField(max_length=500, null=True, blank=True)

    # status_logs
    # status_description logs

    def __str__(self):
        return f"{self.driver}: {self.sacco}"

    def name(self):
        names = f"{self.driver.surname} {self.driver.other_names}"
        return names
