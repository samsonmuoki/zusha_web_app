from django.shortcuts import render

import pyrebase

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from registration.models import Vehicle, Sacco, Driver
from .models import Report
from .forms import ResolveCaseForm
from zusha import settings

# app = Flask("reports")
# Create your views here.


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
    # return HttpResponse("Hello, world. You're at the Reports index page.")
    return render(request, 'reports/index.html')


def view_all_reports_on_map(request):
    """Open map with markers on reported locations."""
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    context = {'reports_query_data': reports_query_data}
    return render(request, 'reports/map.html', context)


def get_reports(request):
    """Fetch all reports."""
    reports = Report.objects.all().order_by('-id')
    reports_dictionary = {}
    for value in range(0, len(reports)):
        data = {
            'regno': reports[value].regno,
            'sacco': reports[value].sacco,
            'speed': reports[value].speed,
            'time': reports[value].time,
            'location': reports[value].location,
            'driver': reports[value].driver,
            'sacco_resolution': reports[value].sacco_resolution,
            'ntsa_resolution': reports[value].ntsa_resolution,
        }
        reports_dictionary.update({reports[value].id: data})

    # page = request.GET.get('page', 1)
    # paginator = Paginator(reports_dictionary, 25)
    # try:
    #     reports_dictionary = paginator.page(page)
    # except PageNotAnInteger:
    #     reports_dictionary = paginator.page(1)
    # except EmptyPage:
    #     reports_dictionary = paginator.page(paginator.num_pages)

    context = {'reports_dictionary': reports_dictionary}

    return render(request, 'reports/reports2.html', context)


# @app.route('/')
def get_reports2(request):
    """Fetch all reports."""
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    # context = {'reports_query_data': reports_query_data}
    reports_dictionary = {}
    for value in range(0, len(reports_query_data)):
        reports_dictionary.update({int(value): reports_query_data[value]})

    # page = request.GET.get('page', 1)
    # paginator = Paginator(reports_dictionary, 25)
    # try:
    #     reports_dictionary = paginator.page(page)
    # except PageNotAnInteger:
    #     reports_dictionary = paginator.page(1)
    # except EmptyPage:
    #     reports_dictionary = paginator.page(paginator.num_pages)

    context1 = {'reports_dictionary': reports_dictionary}

    return render(request, 'reports/reports2.html', context1)


def get_speeding_instance(request, report_id):
    """Fetch a single speeding instance"""
    # report = db.child('Reports').child(report_id).get()
    report = Report.objects.get(id=report_id)
    report_query_data = {
        'regno': report.regno,
        'sacco': report.sacco,
        'speed': report.speed,
        'time': report.time,
        'location': report.location,
        'driver': report.driver,
        'sacco_resolution': report.sacco_resolution,
        'ntsa_resolution': report.ntsa_resolution,
    }
    context = {'report_query_data': report_query_data}
    return render(request, 'reports/single_report.html', context)


def order_reports_by_sacco(request):
    """Sort reports by sacco."""
    reports = Report.objects.all().order_by('sacco')
    reports_dictionary = {}
    for value in range(0, len(reports)):
        data = {
            'regno': reports[value].regno,
            'sacco': reports[value].sacco,
            'speed': reports[value].speed,
            'time': reports[value].time,
            'location': reports[value].location,
            'driver': reports[value].driver,
            'sacco_resolution': reports[value].sacco_resolution,
            'ntsa_resolution': reports[value].ntsa_resolution,
        }
        reports_dictionary.update({reports[value].id: data})

    # page = request.GET.get('page', 1)
    # paginator = Paginator(reports_dictionary, 25)
    # try:
    #     reports_dictionary = paginator.page(page)
    # except PageNotAnInteger:
    #     reports_dictionary = paginator.page(1)
    # except EmptyPage:
    #     reports_dictionary = paginator.page(paginator.num_pages)

    context = {'reports_dictionary': reports_dictionary}

    return render(request, 'reports/reports2.html', context)


def single_sacco_reports(request, sacco):
    """Sort reports by sacco."""
    reports = Report.objects.filter(sacco=sacco).order_by('-time', '-regno')
    reports_dictionary = {}
    for value in range(0, len(reports)):
        data = {
            'regno': reports[value].regno,
            'sacco': reports[value].sacco,
            'speed': reports[value].speed,
            'time': reports[value].time,
            'location': reports[value].location,
            'driver': reports[value].driver,
            'sacco_resolution': reports[value].sacco_resolution,
            'ntsa_resolution': reports[value].ntsa_resolution,
        }
        reports_dictionary.update({reports[value].id: data})

    # page = request.GET.get('page', 1)
    # paginator = Paginator(reports_dictionary, 25)
    # try:
    #     reports_dictionary = paginator.page(page)
    # except PageNotAnInteger:
    #     reports_dictionary = paginator.page(1)
    # except EmptyPage:
    #     reports_dictionary = paginator.page(paginator.num_pages)

    context = {'reports_dictionary': reports_dictionary}

    return render(request, 'reports/sacco_level.html', context)


def resolve_sacco_case(request, regno, sacco, report_id):
    """Resolve all cases for a single vehicle that are reported
    on the same day."""
    # fetch regno
    # fetch date reported
    # Report.objects.filter(
    #     regno=regno,
    #     # time=time
    # ).update(
    #     sacco_resolution=option
    # )
    # reports = Report.objects.filter(regno=regno)
    # reports_dictionary = {}
    # for value in range(0, len(reports)):
    #     data = {
    #         'regno': reports[value].regno,
    #         'sacco': reports[value].sacco,
    #         'speed': reports[value].speed,
    #         'time': reports[value].time,
    #         'location': reports[value].location,
    #         'driver': reports[value].driver,
    #         'sacco_resolution': reports[value].sacco_resolution,
    #         'ntsa_resolution': reports[value].ntsa_resolution,
    #     }
    #     reports_dictionary.update({reports[value].id: data})
    # context = {'reports_dictionary': reports_dictionary}
    # report = Report.objects.get(regno=regno)
    report = Report.objects.get(id=report_id)
    report_query_data = {
        'regno': report.regno,
        'sacco': report.sacco,
        'speed': report.speed,
        'time': report.time,
        'location': report.location,
        'driver': report.driver,
        'sacco_resolution': report.sacco_resolution,
        'ntsa_resolution': report.ntsa_resolution,
    }
    context = {'report_query_data': report_query_data}
    # return render(request, 'reports/single_report.html', context)

    return render(request, 'reports/update_sacco_report_status.html', context)


def update_sacco_report_status(request, regno, sacco):
    """Resolve all cases for a single vehicle that are reported
    on the same day."""
    # fetch regno
    # fetch date reported
    # Report.objects.filter(
    #     regno=regno,
    #     # time=time
    # ).update(
    #     sacco_resolution=option
    # )
    reports = Report.objects.filter(regno=regno)
    reports_dictionary = {}
    for value in range(0, len(reports)):
        data = {
            'regno': reports[value].regno,
            'sacco': reports[value].sacco,
            'speed': reports[value].speed,
            'time': reports[value].time,
            'location': reports[value].location,
            'driver': reports[value].driver,
            'sacco_resolution': reports[value].sacco_resolution,
            'ntsa_resolution': reports[value].ntsa_resolution,
        }
        reports_dictionary.update({reports[value].id: data})
    context = {'reports_dictionary': reports_dictionary}
    # report = Report.objects.get(regno=regno)
    # report_query_data = {
    #     'regno': report.regno,
    #     'sacco': report.sacco,
    #     'speed': report.speed,
    #     'time': report.time,
    #     'location': report.location,
    #     'driver': report.driver,
    #     'sacco_resolution': report.sacco_resolution,
    #     'ntsa_resolution': report.ntsa_resolution,
    # }
    # context = {'report_query_data': report_query_data}
    return render(request, 'reports/resolve_case.html', context)
