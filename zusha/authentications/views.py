from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from .models import SaccoAdmin
from .forms import SaccoAdminAuthenticationForm
from .models import SaccoUser


def login_sacco_admin(request):
    """Login for sacco admin."""
    if request.method == 'POST':
        form = SaccoAdminAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # return HttpResponse(f'Data is valid {username} {password}')
            user = get_object_or_404(
                SaccoUser, username=username, password=password
            )
            sacco = user.sacco
            sacco_id = sacco.id
            if user:
                # return redirect('registrations:saccos_dashboard', sacco)
                return redirect('registrations:saccos_dashboard', sacco_id)
            else:
                return HttpResponse("Invalid login credentials")

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
