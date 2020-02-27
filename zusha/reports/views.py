from django.shortcuts import render

import pyrebase

from django.http import HttpResponse
# from flask import render_template, Flask
# import json


# app = Flask("reports")
# Create your views here.


firebaseConfig = {
    'apiKey': "AIzaSyADbsrYL3TfrkN_jjIQgbUA1JZiJux9-Yw",
    'authDomain': "deep-cascade-240110.firebaseapp.com",
    'databaseURL': "https://deep-cascade-240110.firebaseio.com",
    'projectId': "deep-cascade-240110",
    'storageBucket': "deep-cascade-240110.appspot.com",
    'messagingSenderId': "908598726815",
    'appId': "1:908598726815:web:a6da5cc222b75c52e392aa",
    'measurementId': "G-3QH3QGTQ09"
  }
#   // Initialize Firebase
#   firebase.initializeApp(firebaseConfig);
#   firebase.analytics();
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(
    "samsonmuoki97@gmail.com", "KingJulien97"
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
    context1 = {'reports_dictionary': reports_dictionary}
    # reports_list = []
    # for value in range(0, len(reports_query_data)):
    #     reports_list.append(value[reports_query_data[value]])
    # context2 = {'reports_list': reports_list}

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
