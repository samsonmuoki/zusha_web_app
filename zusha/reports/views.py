from django.shortcuts import render, redirect

import pyrebase

# from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from registration.models import Vehicle, Sacco, Driver
from .models import (
    Report, TrackVehicleReports, TrackSaccoReports, TrackDriverReports
)
# from .forms import ResolveCaseForm
from zusha import settings


firebaseConfig = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': settings.FIREBASE_AUTH_DOMAIN,
    'databaseURL': settings.FIREBASE_DATABASE_URL,
    'projectId': settings.FIREBASE_PROJECT_ID,
    'storageBucket': settings.FIREBASE_STORAGE_BUCKET,
    'messagingSenderId': settings.FIREBASE_MESSAGING_SENDER_ID,
    'appId': settings.FIREBASE_APP_ID,
    'measurementId': settings.FIREBASE_MEASUREMENT_ID
  }

#   // Initialize Firebase
#   firebase.initializeApp(firebaseConfig);
#   firebase.analytics();
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(
    settings.FIREBASE_USER, settings.FIREBASE_PASSWORD
)

db = firebase.database()


def index(request):
    return render(request, 'reports/index.html')


def top_saccos(number):
    """Fetch each vehicle reports."""
    reports_list = TrackVehicleReports.objects.all().order_by(
        '-date', '-count'
    )

    sacco_list = []
    for report in reports_list:
        sacco_list.append(report.sacco)
    reported_saccos = {}
    for sacco in sacco_list:
        reported_saccos.update({sacco: sacco_list.count(sacco)})
    sorted_list = sorted(
        reported_saccos.items(), key=lambda x: x[1], reverse=True
    )
    top_reported_saccos = sorted_list[:number]
    return top_reported_saccos


def top_vehicles(number):
    """Fetch each vehicle reports."""
    reports_list = TrackVehicleReports.objects.all().order_by(
        '-date', '-count'
    )

    vehicle_list = []
    for report in reports_list:
        vehicle_list.append(f"{report.regno}: {report.sacco}")
        # vehicle_list.append(report.regno)
    reported_vehicles = {}
    for vehicle in vehicle_list:
        reported_vehicles.update({vehicle: vehicle_list.count(vehicle)})
    sorted_list = sorted(
        reported_vehicles.items(), key=lambda x: x[1], reverse=True
    )
    top_reported_vehicles = sorted_list[:number]
    return top_reported_vehicles


def top_drivers(number):
    """Sort drivers according to the number of times they are reported."""
    reports_list = TrackDriverReports.objects.all().order_by(
        '-date', '-count'
    )
    driver_list = []
    for report in reports_list:
        driver_list.append(f"{report.driver}: {report.sacco}")
    reported_drivers = {}
    for driver in driver_list:
        reported_drivers.update({driver: driver_list.count(driver)})
    sorted_list = sorted(
        reported_drivers.items(), key=lambda x: x[1], reverse=True
    )
    top_reported_drivers = sorted_list[:number]
    return top_reported_drivers


def top_sacco_vehicles(number, sacco):
    """Fetch each vehicle reports."""
    reports_list = TrackVehicleReports.objects.filter(
        sacco=sacco
    ).order_by(
        '-date', '-count'
    )

    return reports_list[:number]


def top_sacco_drivers(number, sacco):
    """Fetch top reported sacco drivers."""
    reports_list = TrackDriverReports.objects.filter(sacco=sacco).order_by(
        '-date', '-count'
    )
    return reports_list[:number]


def pending_sacco_reports(sacco):
    pending_reports = TrackVehicleReports.objects.filter(
        sacco=sacco, sacco_action='Pending'
    ).order_by(
        '-date'
    ).count()
    return pending_reports


def in_progress_sacco_reports(sacco):
    in_progress_reports = TrackVehicleReports.objects.filter(
        sacco=sacco, sacco_action='In-Progress'
    ).order_by(
        '-date'
    ).count()
    return in_progress_reports


def resolved_sacco_reports(sacco):
    resolved_reports = TrackVehicleReports.objects.filter(
        sacco=sacco, sacco_action='Resolved'
    ).order_by(
        '-date'
    ).count()
    return resolved_reports


def view_all_reports_on_map(request):
    """Open map with markers on reported locations."""
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    context = {'reports_query_data': reports_query_data}
    return render(request, 'reports/map.html', context)


def get_all_reports_list(request):
    """Fetch all reports."""
    reports_list = Report.objects.all().order_by('-id', 'regno')

    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'top_saccos': top_saccos(10),
    }

    return render(request, 'reports/reports2.html', context)


def daily_summary_by_vehicles_reports(request):
    """Fetch each vehicle reports."""
    reports_list = TrackVehicleReports.objects.all().order_by(
        '-date', '-count'
    )

    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'top_saccos': top_saccos(10),
        'top_vehicles': top_vehicles(10),
        'top_drivers': top_drivers(10),
    }

    return render(request, 'reports/summarised_vehicle_reports.html', context)


def daily_summary_by_saccos_reports(request):
    """Summarise all cases for a single day for each sacco reported."""
    reports_list = TrackSaccoReports.objects.all().order_by(
        '-date', '-count'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list
    }

    return render(request, 'reports/summarised_sacco_reports.html', context)


def daily_summary_by_drivers_reports(request):
    """Summarise all cases for a single day for each driver reported."""
    reports_list = TrackDriverReports.objects.all().order_by(
        '-date', '-count'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list
    }

    return render(request, 'reports/summarised_driver_reports.html', context)


def fetch_reports_for_a_vehicle_on_a_specific_day(request, regno, date):
    """Fetch each vehicle reports."""
    reports_list = Report.objects.filter(regno=regno, date=date).order_by(
        '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
        'date': date,
    }

    return render(
        request,
        'reports/specific_date_vehicle_reports.html',
        context
    )


def fetch_reports_for_a_sacco_vehicle_on_a_specific_day(
    request, sacco, regno, date
):
    """Fetch each vehicle reports."""
    report = TrackVehicleReports.objects.get(
        sacco=sacco, regno=regno, date=date
    )
    ntsa_action = report.ntsa_action
    sacco_action = report.sacco_action
    reports_list = Report.objects.filter(
        regno=regno, sacco=sacco, date=date
    ).order_by(
        '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
        'date': date,
        'sacco': sacco,
        'ntsa_action': ntsa_action,
        'sacco_action': sacco_action,
    }

    return render(
        request,
        'reports/specific_date_sacco_vehicle_reports.html',
        context
    )


def fetch_reports_for_a_sacco_on_a_specific_day(request, sacco, date):
    """Fetch each vehicle reports."""
    reports_list = TrackVehicleReports.objects.filter(
        sacco=sacco, date=date
    ).order_by(
        '-date', '-count'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'date': date,
    }

    return render(
        request, 'reports/specific_date_sacco_reports.html', context
    )


def fetch_reports_for_a_driver_on_a_specific_day(request, driver, date):
    """Fetch each vehicle reports."""
    reports_list = Report.objects.filter(driver=driver, date=date).order_by(
        '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list
    }

    return render(
        request, 'reports/specific_date_driver_reports.html', context
    )


def fetch_all_reports_for_a_specific_vehicle(request, regno):
    """Fetch the list of all reports for a certain vehicle."""
    reports_list = Report.objects.filter(regno=regno).order_by(
        '-date', '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
    }

    return render(
        request, 'reports/all_reports_for_a_specific_vehicle.html', context
    )


def fetch_summary_of_all_reports_for_a_specific_vehicle(request, regno):
    """Fetch the list of all reports for a certain vehicle."""
    reports_list = TrackVehicleReports.objects.filter(regno=regno).order_by(
        '-date', '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
    }

    return render(
        request, 'reports/summary_of_all_reports_for_a_vehicle.html', context
    )


def fetch_all_reports_for_a_specific_sacco(request, sacco):
    """Fetch the list of all reports for a certain sacco."""
    reports_list = TrackVehicleReports.objects.filter(sacco=sacco).order_by(
        '-date', '-count',
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'sacco': sacco
    }

    return render(
        request, 'reports/all_reports_for_a_specific_sacco.html', context
    )


def fetch_all_reports_for_a_specific_driver(request, driver):
    """Fetch the list of all reports for a certain driver."""
    reports_list = Report.objects.filter(driver=driver).order_by(
        '-date', '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list
    }

    return render(
        request, 'reports/all_reports_for_a_specific_driver.html', context
    )


def get_speeding_instance(request, regno, report_id):
    """Fetch a single speeding instance"""
    report = Report.objects.get(id=report_id, regno=regno)

    context = {
        'report': report
    }
    return render(
        request, 'reports/single_speeding_instance_report.html', context
    )


def order_reports_by_sacco(request):
    """Sort reports by sacco."""
    reports_list = Report.objects.all().order_by('sacco')

    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 25)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports_list': reports_list,
        'reports': reports,
    }

    return render(request, 'reports/reports2.html', context)


def fetch_all_cases_for_a_specific_sacco_vehicle(request, sacco, regno):
    reports_list = Report.objects.filter(regno=regno, sacco=sacco).order_by(
        '-date',
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 25)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports_list': reports_list,
        'reports': reports,
        'regno': regno,
    }
    return render(
        request,
        'reports/all_cases_for_a_specific_sacco_vehicle.html',
        context
    )


def fetch_all_cases_for_a_specific_sacco_driver(request, sacco, driver):
    reports_list = Report.objects.filter(driver=driver, sacco=sacco).order_by(
        '-date',
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 25)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports_list': reports_list,
        'reports': reports,
        'driver': driver,
    }
    return render(request, 'reports/single_vehicle_cases.html', context)


def fetch_sacco_case(request, regno, report_id, sacco):
    """Resolve all cases for a single vehicle that are reported
    on the same day."""

    report = TrackVehicleReports.objects.get(
        id=report_id, regno=regno, sacco=sacco
    )
    # report.sacco_resolution = status
    # report.save()
    # report = Report.objects.get(id=report_id)

    context = {'report': report}
    return render(request, 'registrations/pending_sacco_reports.html', context)


def update_sacco_case_status(request, regno, sacco, date, status):
    """Update the status of a single case"""
    # report = Report.objects.filter(regno=regno)
    report = TrackVehicleReports.objects.get(
        regno=regno, sacco=sacco, date=date
    )
    report.sacco_action = status
    report.save()
    report = TrackVehicleReports.objects.get(
        sacco=sacco, regno=regno, date=date
    )
    ntsa_action = report.ntsa_action
    sacco_action = report.sacco_action
    reports_list = Report.objects.filter(
        regno=regno, sacco=sacco, date=date
    ).order_by(
        '-id'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
        'date': date,
        'sacco': sacco,
        'ntsa_action': ntsa_action,
        'sacco_action': sacco_action,
    }

    return render(
        request,
        'reports/specific_date_sacco_vehicle_reports.html',
        context
    )


def provide_driver_for_a_reported_case(request, report_id):
    """Enter the name of driver that was reported for speeding.
    Done by sacco admin."""
    pass
