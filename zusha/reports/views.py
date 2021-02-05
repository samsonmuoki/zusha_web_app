from django.shortcuts import (
    render, redirect, get_object_or_404
)

import pyrebase

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from registration.models import Vehicle, Sacco, Driver
from .models import (
    SpeedingInstance, DailyVehicleReport, DailySaccoReport, DailyDriverReport
)
from .forms import (
    # ResolveCaseForm
    ProvideDriverForm,
    UpdateCaseStatusForm
)
from zusha import settings
from registrations.models import Sacco, SaccoDriver, RegisteredDriver

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
    reports_list = DailyVehicleReport.objects.all().order_by(
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
    reports_list = DailyVehicleReport.objects.all().order_by(
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
    reports_list = DailyDriverReport.objects.all().order_by(
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


def top_sacco_vehicles(number, sacco_id):
    """Fetch each vehicle reports."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    reports_list = DailyVehicleReport.objects.filter(
        sacco=sacco
    ).order_by(
        '-date', '-count'
    )

    return reports_list[:number]


def top_sacco_drivers(number, sacco_id):
    """Fetch top reported sacco drivers."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    reports_list = DailyDriverReport.objects.filter(sacco=sacco).order_by(
        '-date', '-count'
    )
    return reports_list[:number]


def pending_sacco_reports(sacco_id):
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    pending_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='Pending'
    ).order_by(
        '-date'
    ).count()
    return pending_reports


def in_progress_sacco_reports(sacco_id):
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    in_progress_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='In Progress'
    ).order_by(
        '-date'
    ).count()
    return in_progress_reports


def resolved_sacco_reports(sacco_id):
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    resolved_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='Resolved'
    ).order_by(
        '-date'
    ).count()
    return resolved_reports


def saccos_list():
    saccos = Sacco.objects.all()
    list_saccos = []
    for sacco in saccos:
        list_saccos.append(sacco.sacco_name)
    return list_saccos


def view_all_reports_on_map(request):
    """Open map with markers on reported locations."""
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    context = {'reports_query_data': reports_query_data}
    return render(request, 'reports/map.html', context)


def get_all_reports_list(request):
    """Fetch all reports."""
    reports_list = SpeedingInstance.objects.all().order_by('-id', 'regno')

    page = request.GET.get('page', 1)
    paginator = Paginator(reports_list, 50)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    saccos = Sacco.objects.all()

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'top_saccos': top_saccos(10),
        'saccos': saccos,
    }

    return render(request, 'reports/reports2.html', context)


def daily_summary_by_vehicles_reports(request):
    """Fetch each vehicle reports."""
    reports_list = DailyVehicleReport.objects.all().order_by(
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
        'saccos_list': saccos_list(),
        'reports': reports,
        'reports_list': reports_list,
        'top_saccos': top_saccos(10),
        'top_vehicles': top_vehicles(10),
        'top_drivers': top_drivers(10),
    }

    return render(request, 'reports/summarised_vehicle_reports.html', context)


def daily_summary_by_saccos_reports(request):
    """Summarise all cases for a single day for each sacco reported."""
    reports_list = DailySaccoReport.objects.all().order_by(
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
    reports_list = DailyDriverReport.objects.all().order_by(
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
    reports_list = SpeedingInstance.objects.filter(
        regno=regno, date=date
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
    }

    return render(
        request,
        'reports/specific_date_vehicle_reports.html',
        context
    )


def fetch_reports_for_a_sacco_vehicle_on_a_specific_day(
    request, sacco_id, regno, date
):
    """Fetch each vehicle reports."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    report = DailyVehicleReport.objects.get(
        sacco=sacco, regno=regno, date=date
    )
    ntsa_action = report.ntsa_action
    sacco_action = report.sacco_action
    reports_list = SpeedingInstance.objects.filter(
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

    if request.method == 'POST':
        form = UpdateCaseStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']

            sacco = Sacco.objects.get(id=sacco_id).sacco_name
            report = DailyVehicleReport.objects.get(
                regno=regno, sacco=sacco, date=date
            )
            report.sacco_action = status
            report.sacco_action_description = description
            report.save()

            return HttpResponse(f"STATUS SUCCESSFULLY UPDATED")

    else:
        form = UpdateCaseStatusForm()

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
        'date': date,
        'sacco': sacco,
        'sacco_id': sacco_id,
        'ntsa_action': ntsa_action,
        'sacco_action': sacco_action,
        'ntsa_description': report.ntsa_action_description,
        'sacco_description': report.sacco_action_description,
        'is_sacco_pending': report.is_sacco_pending,
        'is_all_drivers_submitted': report.is_all_drivers_submitted,
        'form': form,
    }

    return render(
        request,
        'reports/specific_date_sacco_vehicle_reports.html',
        context
    )


def fetch_reports_for_a_sacco_on_a_specific_day(request, sacco, date):
    """Fetch each vehicle reports."""
    reports_list = DailyVehicleReport.objects.filter(
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
    reports_list = SpeedingInstance.objects.filter(
        driver=driver, date=date
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
        'reports_list': reports_list
    }

    return render(
        request, 'reports/specific_date_driver_reports.html', context
    )


def fetch_all_reports_for_a_specific_vehicle(request, regno):
    """Fetch the list of all reports for a certain vehicle."""
    reports_list = SpeedingInstance.objects.filter(regno=regno).order_by(
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

    number = reports_list.count()

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'regno': regno,
        'number': number,
    }

    return render(
        request, 'reports/all_reports_for_a_specific_vehicle.html', context
    )


def fetch_summary_of_all_reports_for_a_specific_vehicle(request, regno):
    """Fetch the list of all reports for a certain vehicle."""
    reports_list = DailyVehicleReport.objects.filter(regno=regno).order_by(
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


def fetch_all_reports_for_a_specific_sacco(request, sacco_id):
    """Fetch the list of all reports for a certain sacco."""
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    reports_list = DailyVehicleReport.objects.filter(sacco=sacco).order_by(
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

    saccos = Sacco.objects.all()

    pending_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='Pending'
    ).order_by('-date')
    in_progress_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='In Progress'
    ).order_by('-date')
    resolved_reports = DailyVehicleReport.objects.filter(
        sacco=sacco, sacco_action='Resolved'
    ).order_by('-date')

    all_reports = DailyVehicleReport.objects.all().count()
    total_cases = reports_list.count()
    pending_reports_percent = pending_reports.count() / (total_cases ) * 100
    in_progress_percent = in_progress_reports.count() / (total_cases) * 100
    resolved_percent = resolved_reports.count() / (total_cases) * 100
    rating = round((all_reports - total_cases) / (all_reports) * 10, 1)

    context = {
        'reports': reports,
        'reports_list': reports_list,
        'sacco': sacco,
        'saccos': saccos,
        'frequently_reported_vehicles': top_sacco_vehicles(10, sacco_id),
        'frequently_reported_drivers': top_sacco_drivers(10, sacco_id),
        'pending_reports': pending_reports,
        'in_progress_reports': in_progress_reports,
        'resolved_reports': resolved_reports,
        'pending_reports_percent': round(pending_reports_percent, 1),
        'in_progress_percent': round(in_progress_percent, 1),
        'resolved_percent': round(resolved_percent, 1),
        'rating': rating,
    }

    return render(
        request, 'reports/all_reports_for_a_specific_sacco.html', context
    )


def fetch_all_reports_for_a_specific_driver(request, driver):
    """Fetch the list of all reports for a certain driver."""
    reports_list = SpeedingInstance.objects.filter(driver=driver).order_by(
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
    report = SpeedingInstance.objects.get(id=report_id, regno=regno)

    context = {
        'report': report
    }
    return render(
        request, 'reports/single_speeding_instance_report.html', context
    )


def order_reports_by_sacco(request):
    """Sort reports by sacco."""
    reports_list = SpeedingInstance.objects.all().order_by('sacco')

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
    reports_list = SpeedingInstance.objects.filter(
        regno=regno, sacco=sacco
    ).order_by(
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
    reports_list = SpeedingInstance.objects.filter(
        driver=driver, sacco=sacco
    ).order_by(
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


def fetch_sacco_case(request, regno, report_id, sacco_id):
    """Resolve all cases for a single vehicle that are reported
    on the same day."""
    sacco = Sacco.objects.get(id=sacco_id)

    if request.method == 'POST':
        form = ProvideDriverForm(data=request.POST)
        if form.is_valid():
            driver_id = form.cleaned_data['driver']

            driver = get_object_or_404(RegisteredDriver, national_id=driver_id)
            sacco_driver = get_object_or_404(
                SaccoDriver, driver=driver, sacco=sacco
            )
            rep = SpeedingInstance.objects.get(id=report_id)

            rep.driver = sacco_driver
            rep.save()
            context = {
                'sacco_id': sacco_id,
                'report': rep,
                'sacco_driver': sacco_driver,
            }
            return render(
                request,
                'reports/single_sacco_report.html',
                context,
            )

    else:
        form = ProvideDriverForm()
    report = SpeedingInstance.objects.get(
        id=report_id,
    )
    # sacco = Sacco.objects.get(id=sacco_id)
    drivers_list = SaccoDriver.objects.filter(sacco=sacco)
    return render(
        request, 'reports/single_sacco_report.html',
        {
            'form': form,
            'report': report,
            'drivers': drivers_list,
            'sacco_id': sacco_id,
        }
    )


def update_sacco_case_status(request, regno, sacco_id, date, status):
    """Update the status of a single case"""
    # report = Report.objects.filter(regno=regno)
    sacco = Sacco.objects.get(id=sacco_id).sacco_name
    report = DailyVehicleReport.objects.get(
        regno=regno, sacco=sacco, date=date
    )
    report.sacco_action = status
    report.save()
    report = DailyVehicleReport.objects.get(
        sacco=sacco, regno=regno, date=date
    )
    ntsa_action = report.ntsa_action
    sacco_action = report.sacco_action
    reports_list = SpeedingInstance.objects.filter(
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
        'sacco_id': sacco_id,
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
    if request.method == 'POST':
        form = ProvideDriverForm(data=request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']

            rep = SpeedingInstance.objects.get(id=report_id)

            rep.driver = driver
            rep.save()
            return render(
                request,
                'reports/single_sacco_report.html',
                {'report': rep},
            )

    else:
        form = ProvideDriverForm()
    report = SpeedingInstance.objects.get(
        id=report_id,
    )
    return render(
        request, 'reports/single_sacco_report.html',
        {
            'form': form,
            'report': report,
        }
    )


def trial(request):
    """Enter the name of driver that was reported for speeding.
    Done by sacco admin."""
    if request.method == 'POST':
        form = UpdateCaseStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            # pdb.set_trace()

            return HttpResponse(f"{status} {description}")

    else:
        form = UpdateCaseStatusForm()
    return render(
        request, 'reports/update_sacco_report_status.html',
        {
            'form': form,
        }
    )
