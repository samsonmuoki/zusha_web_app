from django.shortcuts import render

import pyrebase

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from flask import render_template, Flask
# import json

# from registration.models import Vehicle, Sacco, Driver
from registrations.models import Vehicle, Sacco, Driver
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


def get_reports(request):
    """Fetch all reports."""
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    context = {'reports_query_data': reports_query_data}
    return render(request, 'reports/reports.html', context)
    # return render(request, 'reports/reports.html')


def view_map(request):
    """Open map with markers on reported locations."""
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    context = {'reports_query_data': reports_query_data}
    return render(request, 'reports/map.html', context)


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
    # reports_list = []
    # indexed_report = []
    # indexed_reports = []
    # for value in range(0, len(reports_query_data)):
    #     # reports_list.append(reports_query_data[value])
    #     indexed_report.append(value)
    #     # indexed_report.append(reports_query_data[value])
    #     # indexed_report = reports_query_data[value].update({"Report_id": value})
    #     reports_list.append(value)
    #     context2 = {'reports_list': reports_list}

    return render(request, 'reports/reports2.html', context1)


def get_speeding_instance(request, report_id):
    """Fetch a single speeding instance"""
    report = db.child('Reports').child(report_id).get()
    report_query_data = report.val()
    context = {'report_query_data': report_query_data}
    return render(request, 'reports/single_report.html', context)


# def reports_by_sacco(request):
#     """Sort reports by sacco."""
#     reports_by_sacco = db.child("Reports").order_by_child("sacco").equal_to("lopha").get()
#     sacco_query_data = reports_by_sacco.val()
#     context = {'sacco_query_data': sacco_query_data}
#     return render(request, 'reports/sacco_level.html', context)


def reports_by_sacco(request, sacco):
    """Sort reports by sacco."""
    # reports_by_sacco = db.child("Reports").order_by_child("sacco").equal_to("lopha").get()
    # report = db.child("Reports").child(10).child("Sacco").get()
    reports = db.child("Reports").get()
    reports_query_data = reports.val()
    # sacco_query_data = reports_by_sacco.val()
    # context = {'reports_query_data': reports_query_data}
    # sacco_reports = []
    # for report in reports_query_data:
    #     if report['Sacco'] == sacco:
    #         sacco_reports.append(report)
    # context = {'sacco_reports': sacco_reports}
    reports_dictionary = {}
    for value in range(0, len(reports_query_data)):
        # reports_dictionary.update({int(value): reports_query_data[value]["Sacco"]})
        if reports_query_data[value]["Sacco"] == sacco:
            # sacco_reports.append(reports_query_data[value])
            reports_dictionary.update({int(value): reports_query_data[value]})
    context = {'reports_dictionary': reports_dictionary}
    # context = {'sacco_reports': sacco_reports}
    return render(request, 'reports/sacco_level.html', context)
