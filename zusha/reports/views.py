from django.shortcuts import render

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
        'reports_list': reports_list
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
        'reports_list': reports_list
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


def resolve_sacco_case(request, report_id, sacco, status):
    """Resolve all cases for a single vehicle that are reported
    on the same day."""

    report = TrackVehicleReports.objects.get(id=report_id, sacco=sacco)
    report.sacco_resolution = status
    report.save()
    report = Report.objects.get(id=report_id)

    context = {'report': report}
    return render(request, 'reports/update_sacco_report_status.html', context)


def update_sacco_case_status(request, regno, sacco, report_id, status):
    """Update the status of a single case"""
    # report = Report.objects.filter(regno=regno)
    report = Report.objects.get(id=report_id)
    report.sacco_resolution = status
    report.save()
    report = Report.objects.get(id=report_id)

    context = {'report': report}
    return render(request, 'reports/update_sacco_report_status.html', context)


def provide_driver_for_a_reported_case(request, report_id):
    """Enter the name of driver that was reported for speeding.
    Done by sacco admin."""
    pass
