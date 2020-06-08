from django import forms


class SaccoAdminForm(forms.Form):
    """Viewset for sacco admin registration."""
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    # id_no = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=10)
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=100)


class SaccoAdminAuthenticationForm(forms.Form):
    """Sacco Login Form."""
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=100)
