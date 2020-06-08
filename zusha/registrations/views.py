# import pyrebase

from django.contrib.auth import (
    # authenticate,
    login, logout
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from qr_code.qrcode.utils import QRCodeOptions

from .models import Sacco, Vehicle, Driver, SaccoDriver, SaccoVehicle
from .forms import VehicleForm, DriverForm
from reports.views import (
    top_sacco_vehicles,
    top_sacco_drivers,
    pending_sacco_reports,
    in_progress_sacco_reports,
    resolved_sacco_reports,
)


def index(request):
    return render(request, "registrations/home.html")


def saccos_dashboard(request, sacco):
    context = {
        'sacco': sacco,
        'pending_reports': pending_sacco_reports(sacco),
        'in_progress_reports': in_progress_sacco_reports(sacco),
        'resolved_sacco_reports': resolved_sacco_reports(sacco),
        'top_sacco_vehicles': top_sacco_vehicles(20, sacco),
        'top_sacco_drivers': top_sacco_drivers(20, sacco),
    }
    return render(request, "registrations/sacco_dashboard.html", context)


def get_all_saccos(request):
    """Fetch all registered saccos."""
    saccos = Sacco.objects.order_by('sacco_name')

    page = request.GET.get('page', 1)
    paginator = Paginator(saccos, 25)
    try:
        saccos = paginator.page(page)
    except PageNotAnInteger:
        saccos = paginator.page(1)
    except EmptyPage:
        saccos = paginator.page(paginator.num_pages)

    context = {'saccos': saccos}
    return render(request, 'registrations/saccos.html', context)


def get_all_drivers(request):
    """Fetch all drivers details."""
    drivers = SaccoDriver.objects.order_by('-driver_id')

    page = request.GET.get('page', 1)
    paginator = Paginator(drivers, 25)
    try:
        drivers = paginator.page(page)
    except PageNotAnInteger:
        drivers = paginator.page(1)
    except EmptyPage:
        drivers = paginator.page(paginator.num_pages)

    context = {'drivers': drivers}
    return render(request, 'registrations/drivers.html', context)


def get_all_vehicles(request):
    """Fetch all vehicles."""
    vehicles = SaccoVehicle.objects.order_by('sacco')

    page = request.GET.get('page', 1)
    paginator = Paginator(vehicles, 10)
    try:
        vehicles = paginator.page(page)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    context = {'vehicles': vehicles}
    return render(request, 'registrations/vehicles.html', context)


def get_a_single_vehicle(request, registration_number):
    """Fetch a single sacco details."""
    ntsa_vehicle = Vehicle.objects.get(registration_number=registration_number)
    sacco_vehicle = SaccoVehicle.objects.get(vehicle=ntsa_vehicle)
    reg_no = ntsa_vehicle.registration_number
    sacco = sacco_vehicle.sacco
    email = Sacco.objects.get(sacco_name=sacco).email
    qr_code_values = f"{reg_no},{sacco},{email}"
    context = dict(
        regno=ntsa_vehicle.registration_number,
        vehicle=sacco_vehicle,
        qr_code_values=qr_code_values,
        qr_options=QRCodeOptions(
            size='m', border=6, error_correction='L', image_format='png',
        ),
    )
    return render(request, 'registrations/vehicle_details.html', context)


def get_driver_details(request, driver_id):
    """Fetch a specific driver's details."""
    driver = get_object_or_404(Driver, driver_id=driver_id)
    context = {'driver': driver}
    return render(request, 'registrations/driver_details.html', context)


def signup_sacco_admin(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login the user in
            login(request, user)
            return redirect('registrations:saccos_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registrations/signup.html', {'form': form})


def login_sacco_admin(request):
    """Login for Sacco Admin."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login the user
            user = form.get_user()
            login(request, user)
            return redirect('registrations:saccos_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registrations/login.html', {'form': form})


def logout_sacco_admin(request):
    """Logout sacco admin."""
    if request.method == 'POST':
        logout(request)
        return redirect('registrations:saccos')


def add_vehicle(request):
    """Sacco admins add the list of vehicles they operate."""
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            sacco_name = form.cleaned_data['sacco']
            regno = form.cleaned_data['regno']

            vehicle = get_object_or_404(Vehicle, registration_number=regno)
            sacco = get_object_or_404(Sacco, sacco_name=sacco_name)
            if sacco:
                SaccoVehicle.objects.create(
                    vehicle=vehicle,
                    sacco=sacco
                )
                return HttpResponse('Vehicle successfully Added')
            # TODO provide useful response below if invalid sacco is provided
            # else:
            #     return HttpResponse('The sacco provided does not exist')
    else:
        form = VehicleForm()
        return render(
            request, 'registrations/register_vehicle.html',
            {'form': form}
        )


def add_driver(request):
    """Sacco admins add the list of vehicles they operate."""
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            driver_id = form.cleaned_data['driver_id']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            sacco_name = form.cleaned_data['sacco']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            sacco = get_object_or_404(Sacco, sacco_name=sacco_name)
            driver = get_object_or_404(Driver, driver_id=driver_id)

            SaccoDriver.objects.create(
                driver=driver,
                sacco=sacco,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number
            )
            return HttpResponse('Driver successfully Added')
            # TODO provide useful response below if invalid sacco
            # or driver is provided
            # else:
            #     return HttpResponse('The sacco provided does not exist')
    else:
        form = VehicleForm()
        return render(
            request, 'registrations/add_driver.html',
            {'form': form}
        )
