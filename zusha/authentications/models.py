from django.db import models
from registrations.models import Sacco


class SaccoUser(models.Model):
    """."""
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    # id_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT)
