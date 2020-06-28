from django import forms

SACCO_DRIVER_STATUS_OPTIONS = [
    ('Approved', ('Approved to operate')),
    ('Suspended', ('Suspended for the time being')),
    ('Blacklisted', ('Blacklisted from operating'))
]


class VehicleForm(forms.Form):
    # sacco = forms.CharField(label="Sacco", max_length=100)
    regno = forms.CharField(label="Registration Number", max_length=7)

    # def get_sacco(self):
    #     """Return the name of the sacco."""
    #     return self.sacco

    def get_regno(self):
        """Return the regno of the vehicle."""
        return self.regno


class DriverForm(forms.Form):
    """Viewset for add driver."""
    national_id = forms.CharField(max_length=8)
    # first_name = forms.CharField(max_length=10)
    # last_name = forms.CharField(max_length=10)
    # # sacco = forms.CharField(max_length=10)
    # email = forms.CharField(max_length=15)
    # phone_number = forms.CharField(max_length=12)


class UpdateSaccoDriverStatusForm(forms.Form):
    """."""
    status = forms.CharField(
        widget=forms.Select(choices=SACCO_DRIVER_STATUS_OPTIONS)
    )
    description = forms.CharField(widget=forms.Textarea)


class SearchDriverIdForm(forms.Form):
    """Search for a driver."""
    national_id = forms.CharField(max_length=10, help_text="Enter driver id")
