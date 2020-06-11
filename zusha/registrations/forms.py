from django import forms


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
    driver_id = forms.CharField(max_length=8)
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    # sacco = forms.CharField(max_length=10)
    email = forms.CharField(max_length=15)
    phone_number = forms.CharField(max_length=12)
