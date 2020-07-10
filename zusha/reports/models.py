from django.db import models
from registrations.models import SaccoDriver


PENDING = 'Pending'
IN_PROGRESS = 'In Progress'
RESOLVED = 'Resolved'

RESOLUTION_OPTIONS = [
    (PENDING, ('No action was taken')),
    (IN_PROGRESS, ('Currently being resolved')),
    (RESOLVED, ('Corrective Action was taken'))
]


class SpeedingInstance(models.Model):
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
    location = models.CharField(max_length=100, null=True)
    # driver = models.CharField(
    #     max_length=20, null=True, blank=True
    # )  # to be updated by sacco
    driver = models.ForeignKey(
        SaccoDriver, on_delete=models.PROTECT, null=True
    )  # updated by sacco admin for each case that is reported

    def __str__(self):
        return f"{self.regno} {self.speed}"


class DailyVehicleReport(models.Model):
    """Summary for all vehicles reported on a single day."""
    regno = models.CharField(max_length=10)
    sacco = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=False)
    count = models.IntegerField(default=0, editable=False)
    ntsa_action = models.CharField(
        max_length=20, choices=RESOLUTION_OPTIONS, default=PENDING
    )
    ntsa_action_description = models.TextField(max_length=500, null=True)
    sacco_action = models.CharField(
        max_length=20, choices=RESOLUTION_OPTIONS, default=PENDING
    )
    sacco_action_description = models.TextField(
        max_length=500, null=True, blank=True
    )

    def __str__(self):
        return "{} {} {} {} {} {}".format(
            self.regno, self.sacco, self.date, self.count, self.ntsa_action,
            self.sacco_action,
        )

    def is_sacco_pending(self):
        if self.sacco_action == PENDING:
            return True

    def is_all_drivers_submitted(self):
        """Check whether all drivers have been submitted."""
        reports = SpeedingInstance.objects.filter(
            regno=self.regno,
            date=self.date
        )
        all_drivers_submitted = True
        for report in reports:
            if report.driver is None:
                all_drivers_submitted = False

        return all_drivers_submitted


class DailySaccoReport(models.Model):
    """Summary for all saccos reported on a single day."""
    sacco = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=False)
    count = models.IntegerField(default=0)
    # show overall number of cases this is going to be shown in a view

    def __str__(self):
        return f"{self.sacco} {self.date} {self.count}"


class DailyDriverReport(models.Model):
    """Summary for all drivers reported on a single day."""
    # driver = models.CharField(max_length=20, null=True, blank=True)
    driver = models.ForeignKey(
        SaccoDriver, on_delete=models.CASCADE, null=True
    )
    sacco = models.CharField(max_length=20)
    regno = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    ntsa_action = models.CharField(max_length=20, choices=RESOLUTION_OPTIONS)
    ntsa_action_description = models.TextField(
        max_length=500, null=True, blank=True
    )
    count = models.IntegerField(default=0)
