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

from .models import (
    Sacco, Vehicle, RegisteredDriver, SaccoDriver, SaccoVehicle
)
from .forms import VehicleForm, DriverForm
from reports.views import (
    top_sacco_vehicles,
    top_sacco_drivers,
    pending_sacco_reports,
    in_progress_sacco_reports,
    resolved_sacco_reports,
)
from reports.models import (
    SpeedingInstance, DailyVehicleReport, DailySaccoReport, DailyDriverReport
)


def index(request):
    return render(request, "registrations/home.html")


def saccos_dashboard(request, sacco_id):
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    context = {
        'sacco_header': sacco.upper(),
        'sacco': sacco,
        'sacco_id': sacco_id,
        'pending_reports': pending_sacco_reports(sacco_id),
        'in_progress_reports': in_progress_sacco_reports(sacco_id),
        'resolved_sacco_reports': resolved_sacco_reports(sacco_id),
        # 'top_sacco_vehicles': top_sacco_vehicles(20, sacco),
        # 'top_sacco_drivers': top_sacco_drivers(20, sacco),
    }
    return render(request, "registrations/sacco_dashboard.html", context)


def fetch_pending_reports_for_a_sacco(request, sacco_id):
    """."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    pending_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='Pending'
    ).order_by('-date')
    context = {
        'sacco_id': sacco_id,
        'pending_sacco_reports': pending_reports,
    }
    return render(
        request,
        'registrations/pending_sacco_reports.html',
        context
    )


def fetch_in_progress_reports_for_a_sacco(request, sacco_id):
    """."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    in_progress_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='In-Progress'
    ).order_by('-date')
    context = {
        'sacco_id': sacco_id,
        'in_progress_sacco_reports': in_progress_reports,
    }
    return render(
        request,
        'registrations/in_progress_sacco_reports.html',
        context
    )


def fetch_resolved_reports_for_a_sacco(request, sacco_id):
    """."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    resolved_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='Resolved'
    ).order_by('-date')
    context = {
        'sacco_id': sacco_id,
        'resolved_sacco_reports': resolved_reports,
    }
    return render(
        request,
        'registrations/resolved_sacco_reports.html',
        context
    )


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


def saccos_list():
    """Fetch all registered saccos."""
    saccos = Sacco.objects.order_by('sacco_name')
    list_saccos = []
    for sacco in saccos:
        list_saccos.append(sacco.sacco_name)

    return list_saccos


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

    context = {
        'vehicles': vehicles,
        'saccos_list': saccos_list(),
    }
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
        license_status=ntsa_vehicle.license_status.upper(),
        qr_code_values=qr_code_values,
        qr_options=QRCodeOptions(
            size='m', border=6, error_correction='L', image_format='png',
        ),
    )
    return render(request, 'registrations/vehicle_details.html', context)


def get_driver_details(request, driver_id):
    """Fetch a specific driver's details."""
    driver = get_object_or_404(RegisteredDriver, driver_id=driver_id)
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


def add_vehicle(request, sacco_id):
    """Sacco admins add the list of vehicles they operate."""
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            regno = form.cleaned_data['regno']

            vehicle = get_object_or_404(Vehicle, registration_number=regno)
            is_for_public_transport = vehicle.is_for_public_transport()
            is_approved = vehicle.is_approved()
            # sacco = get_object_or_404(Sacco, id=sacco_id)
            context = {
                'sacco_id': sacco_id,
                "vehicle": vehicle,
                'public_transport': is_for_public_transport,
                'is_approved': is_approved,
            }
            return render(
                request, 'registrations/register_vehicle.html', context
            )
    else:
        form = VehicleForm()
    return render(
        request, 'registrations/register_vehicle.html',
        {'form': form}
    )


def confirm_vehicle(request, sacco_id, regno):
    """."""
    vehicle = get_object_or_404(
        Vehicle, registration_number=regno
    )
    sacco = get_object_or_404(Sacco, id=sacco_id)
    SaccoVehicle.objects.create(
        vehicle=vehicle,
        sacco=sacco,
    )
    return HttpResponse('VEHICLE SUCCESSFULLY ADDED')


def add_driver(request, sacco_id):
    """Sacco admins add the list of vehicles they operate."""
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id']

            sacco = get_object_or_404(Sacco, id=sacco_id)

            driver = get_object_or_404(
                RegisteredDriver, national_id=national_id
            )
            is_approved = driver.is_approved()

            context = {
                'sacco_id': sacco_id,
                'sacco': sacco.sacco_name.upper(),
                'driver': driver,
                'is_approved': is_approved,
            }
            return render(
                request, 'registrations/add_driver.html', context
            )
    else:
        form = DriverForm()
    return render(
        request, 'registrations/add_driver.html',
        {'form': form}
    )


def confirm_driver(request, sacco_id, driver_id):
    """."""
    driver = get_object_or_404(
        RegisteredDriver, national_id=driver_id
    )
    sacco = get_object_or_404(Sacco, id=sacco_id)
    SaccoDriver.objects.create(
        driver=driver,
        sacco=sacco,
    )
    return HttpResponse('DRIVER SUCCESSFULLY ADDED')
