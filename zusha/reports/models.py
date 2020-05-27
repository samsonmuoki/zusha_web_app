from django.db import models


PENDING = 'Pending'
IN_PROGRESS = 'In Progress'
RESOLVED = 'Resolved'

RESOLUTION_OPTIONS = [
    (PENDING, ('No action was taken')),
    (IN_PROGRESS, ('Currently being resolved')),
    (RESOLVED, ('Corrective Action was taken'))
]


class Report(models.Model):
    """Store cases reported by passengers."""
    regno = models.CharField(max_length=10, null=True)
    sacco = models.CharField(max_length=10, null=True)
    speed = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True
    )
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
    sacco_resolution = models.CharField(
        max_length=20,
        choices=RESOLUTION_OPTIONS,
        default=PENDING
    )
    ntsa_resolution = models.CharField(
        max_length=20,
        choices=RESOLUTION_OPTIONS,
        default=PENDING
    )

    def __str__(self):
        return f"{self.regno} {self.speed}"
