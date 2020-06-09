from django.db import models


PENDING = 'Pending'
IN_PROGRESS = 'In-Progress'
RESOLVED = 'Resolved'

RESOLUTION_OPTIONS = [
    (PENDING, ('No action was taken')),
    (IN_PROGRESS, ('Currently being resolved')),
    (RESOLVED, ('Corrective Action was taken'))
]


class Report(models.Model):
    """Store cases reported by passengers."""
    regno = models.CharField(max_length=10, null=True)
    sacco = models.CharField(max_length=20, null=True)
    speed = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.DateTimeField(
        auto_now=False, auto_now_add=False
    )
    date = models.DateField(
        auto_now=False, auto_now_add=False,
    )
    location = models.CharField(max_length=100, null=True)
    driver = models.CharField(
        max_length=20, null=True, blank=True
    )  # to be updated by sacco

    def __str__(self):
        return f"{self.regno} {self.speed}"


class TrackVehicleReports(models.Model):
    """Summary for all vehicles reported on a single day."""
    regno = models.CharField(max_length=10)
    sacco = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=False)
    count = models.IntegerField(default=0)
    ntsa_action = models.CharField(
        max_length=20, choices=RESOLUTION_OPTIONS, default=PENDING
    )
    sacco_action = models.CharField(
        max_length=20, choices=RESOLUTION_OPTIONS, default=PENDING
    )

    def __str__(self):
        return "{} {} {} {} {} {}".format(
            self.regno, self.sacco, self.date, self.count, self.ntsa_action,
            self.sacco_action,
        )


class TrackSaccoReports(models.Model):
    """Summary for all saccos reported on a single day."""
    sacco = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=False)
    count = models.IntegerField(default=0)
    # number of cases pending
    # number or cases in progress
    # number of cases in resolved
    # show overall number of cases this is going to be shown in a view

    def __str__(self):
        return f"{self.sacco} {self.date} {self.count}"


class TrackDriverReports(models.Model):
    """Summary for all drivers reported on a single day."""
    driver = models.CharField(max_length=20, null=True, blank=True)
    sacco = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    count = models.IntegerField(default=0)
