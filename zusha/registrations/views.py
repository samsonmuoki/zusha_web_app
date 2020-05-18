# import pyrebase

from django.shortcuts import render, get_object_or_404

# Create your views here.
# from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from qr_code.qrcode.utils import ContactDetail  # QRCodeOptions
from qr_code.qrcode.utils import QRCodeOptions

from .models import Sacco, Vehicle, Driver


def index(request):
    return render(request, "registrations/home.html")


def get_all_saccos(request):
    """Fetch all registered saccos."""
    saccos = Sacco.objects.order_by('-sacco_name')

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
    drivers = Driver.objects.order_by('-driver_id')

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
    vehicles = Vehicle.objects.order_by('registration_number')

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
    vehicle = Vehicle.objects.get(registration_number=registration_number)
    reg_no = vehicle.registration_number
    sacco = vehicle.sacco
    email = sacco.email
    qr_code_values = f"{reg_no},{sacco},{email}"
    # qr_list = [vehicle.registration_number, vehicle.sacco]
    # import pdb;
    # pdb.set_trace()
    context = dict(
        vehicle=vehicle,
        # qr_list=qr_list,
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
