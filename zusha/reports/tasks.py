from __future__ import absolute_import, unicode_literals
import pyrebase

from django.core.mail import send_mail

from celery import shared_task, Celery
from celery.decorators import periodic_task
from celery.schedules import crontab
# from celery.contrib import rdb

from registration.models import Sacco, Driver, Vehicle

# from registration.models import LICENSE_STATUS

app = Celery('tasks', backend='rpc://', broker='pyamqp://')

# app.conf.timezone = 'UTC'


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


# @shared_task
# def blacklist_gari():
#     reports = db.child('Reports').get()
#     reports_query_data = reports.val()
#     reports_list = []
#     vehicle = Vehicle.objects.get(registration_number="KAA")
#     for report in reports_query_data:
#         if report["RegNo"] == f"{vehicle.registration_number} ":
#             reports_list.append(report)
#     # rdb.set_trace()
#     if len(reports_list) > 1:
#         # vehicle.license_status = LICENSE_STATUS.BLACKLISTED
#         vehicle.license_status = "blacklisted"
#         vehicle.save()


@shared_task
def blacklist_gari2():
    # Fecth all registered vehicles
    # Fetch all reports
    # If count for each vehicle is above threshold, blacklist the vehicle.
    vehicles = Vehicle.objects.all()
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    for vehicle in vehicles:
        reports_list = []
        for report in reports_query_data:
            if report["RegNo"] == f"{vehicle.registration_number}":
                reports_list.append(report)
        if len(reports_list) > 1:
            vehicle.license_status = "blacklisted"
            vehicle.save()


# @periodic_task
@shared_task
def send_alerts():
    send_mail(
        'ZUSHA REPORT',
        'Your vehicle has been reported',
        'samsonmuoki97@gmail.com',
        ['samsonmuoki97@gmail.com'],
        fail_silently=False,
    )


# @periodic_task
@shared_task
def blacklist_vehicles():
    # Fecth all registered vehicles
    # Fetch all reports
    # If count for each vehicle is above threshold, blacklist the vehicle.
    vehicles = Vehicle.objects.all()
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    for vehicle in vehicles:
        reports_list = []
        for report in reports_query_data:
            if report["RegNo"] == f"{vehicle.registration_number}":
                reports_list.append(report)
        if len(reports_list) > 1:
            vehicle.license_status = "BLACKLISTED"
            vehicle.save()


# @periodic_task
@shared_task
def blacklist_sacco(sacco):
    # Fetch all reports
    # Fecth all registered saccos
    # If count for each sacco is above threshold, blacklist the sacco.
    saccos = Sacco.objects.all()
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    for sacco in saccos:
        reports_list = []
        for report in reports_query_data:
            if report["Sacco"] == sacco.name:
                reports_list.append(report)
        if len(reports_list) > 1:
            sacco.license_status = "BLACKLISTED"
            sacco.save()


# @periodic_task
@shared_task
def blacklist_drivers():
    # Fetch all reports
    # Fecth all registered saccos
    # If count for each sacco is above threshold, blacklist the sacco.
    drivers = Driver.objects.all()
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    for driver in drivers:
        reports_list = []
        for report in reports_query_data:
            if report["Driver"] == driver.name:
                reports_list.append(report)
        if len(reports_list) > 1:
            driver.license_status = "BLACKLISTED"
            driver.save()


# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'send-notifications-every-minute': {
#         'task': 'tasks.add',
#         # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'schedule': crontab(),  # execute every minute
#         'args': (16, 16),
#     },
# }
