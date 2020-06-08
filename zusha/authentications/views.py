from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from .models import SaccoAdmin
from .forms import SaccoAdminAuthenticationForm


def login_sacco_admin(request):
    """Login for sacco admin."""
    if request.method == 'POST':
        form = SaccoAdminAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            return HttpResponse(f'Data is valid {username} {password}')

    else:
        form = SaccoAdminAuthenticationForm()
        return render(
            request,
            'authentications/login_sacco_admin.html',
            {'form': form}
        )


def sacco_admin_signup(request):
    """."""
    pass
