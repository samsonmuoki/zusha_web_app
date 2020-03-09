# import pyrebase

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Sacco, Vehicle, Driver


def index(request):
    # return HttpResponse("Hello, world. You're at the Registration index page.")
    return render(request, "registration/home.html")


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
    return render(request, 'registration/saccos.html', context)


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
    return render(request, 'registration/drivers.html', context)


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
    return render(request, 'registration/vehicles.html', context)


def get_driver_details(request, driver_id):
    """Fetch a specific driver's details."""
    driver = get_object_or_404(Driver, driver_id=driver_id)
    context = {'driver': driver}
    return render(request, 'registration/driver_details.html', context)
