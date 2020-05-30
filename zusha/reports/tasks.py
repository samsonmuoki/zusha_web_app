from __future__ import absolute_import, unicode_literals
import pyrebase

# from django.core.mail import send_mail

from celery import shared_task, Celery
# from celery.decorators import periodic_task
# from celery.schedules import crontab

# from django.utils import timezone
from datetime import (
    date
    # timedelta,
    # datetime,
)
# import datetime
import pytz

# from celery.contrib import rdb
from zusha import settings

from registrations.models import Sacco, Driver, Vehicle
from .models import (
    Report, TrackVehicleReports, TrackSaccoReports, TrackDriverReports
)

# from registration.models import LICENSE_STATUS

app = Celery('tasks', backend='rpc://', broker='pyamqp://')

# app.conf.timezone = 'UTC'


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


@shared_task
def update_reports_db():
    reports = db.child('Reports').get()
    reports_query_data = reports.val()
    for report in reports_query_data:
        # driver = report['Driver']
        location = report['Location']
        regno = report['RegNo']
        sacco = report['Sacco']
        speed = report['Speed']
        time = report['Time'].replace(' at', '').replace('.', '-')
        date_list = time.replace(' ', '-').replace(':', '-').split('-')
        # date = datetime.date(
        day = date(
            int(date_list[0]), int(date_list[1]), int(date_list[2])
        )

        Report.objects.get_or_create(
            regno=regno,
            sacco=sacco,
            speed=speed,
            time=time,
            location=location,
            date=day
        )


@shared_task
def track_each_vehicle_reports():
    reports = Report.objects.all()
    for report in reports:
        case_count = Report.objects.filter(regno=report.regno).count()
        tracker, created = TrackVehicleReports.objects.get_or_create(
            regno=report.regno,
            date=report.date,
            sacco=report.sacco,
            defaults={'count': case_count},
        )


@shared_task
def track_each_sacco_reports():
    reports = Report.objects.all()
    for report in reports:
        case_count = Report.objects.filter(sacco=report.sacco).count()
        tracker, created = TrackSaccoReports.objects.get_or_create(
            sacco=report.sacco,
            date=report.date,
            defaults={'count': case_count},
        )


@shared_task
def track_each_driver_reports():
    reports = Report.objects.all()
    for report in reports:
        case_count = Report.objects.filter(sacco=report.sacco).count()
        tracker, created = TrackDriverReports.objects.get_or_create(
            driver=report.driver,
            date=report.date,
            defaults={'count': case_count},
        )


@shared_task
def blacklist_vehicles():
    vehicles = Vehicle.objects.all()
    reports = Report.objects.all()
    for vehicle in vehicles:
        reports_list = []
        for report in reports:
            if report.regno == vehicle.registration_number:
                reports_list.append(report)
        if len(reports_list) > 5:
            vehicle.license_status = "blacklisted"
            vehicle.save()


utc = pytz.utc


@shared_task
def blacklist_saccos():
    saccos = Sacco.objects.all()
    reports = Report.objects.all()
    for sacco in saccos:
        reports_list = []
        for report in reports:
            if report.sacco == sacco.sacco_name:
                reports_list.append(report)
        if len(reports_list) > 5:
            sacco.license_status = "BLACKLISTED"
            sacco.save()


# TODO optimise driver reporting
# @shared_task
# def blacklist_drivers():
#     drivers = Driver.objects.all()
#     reports = Report.objects.all()
#     for driver in drivers:
#         reports_list = []
#         for report in reports:
#             if report.driver_id == driver.driver_id:
#                 reports_list.append(report)
#         if len(reports_list) > 1:
#             driver.license_status = "BLACKLISTED"
#             driver.save()


# @periodic_task
# @shared_task
# def send_alerts():
#     """Send notifications to Saccos whose vehicles have been reported."""
#     # Fetch each sacco's email from the local database.
#     saccos = Sacco.objects.all()
#     # Fetch all reports from the firebase
#     reports = db.child('Reports').get()
#     reports_query_data = reports.val()
#     # Filter the reports send in the last minute
#     # all_latest_reports = []
#     reports_dictionary = {}

#     for value in range(0, len(reports_query_data)):
#         time_str = datetime.strptime(reports_query_data[value]['Time'], '%Y.%m.%d at %H:%M:%S')
#         if timezone.now().replace(tzinfo=None)-time_str < timedelta(hours=1):
#             reports_dictionary.update({int(value): reports_query_data[value]})
#     # rdb.set_trace()

#     # for sacco in saccos:
#     for key, value in reports_dictionary.items():
#         for sacco in saccos:
#             if value["Sacco"] == sacco.sacco_name:
#                 email_subject = "ZUSHA COMPLAINT"
#                 email_message = f"Vehicle REG: {value['RegNo']} belonging to your sacco, has been reported for overspeeding at {value['Speed']} KM/H in this Location {value['Location']}"
#                 send_mail(
#                     email_subject,
#                     email_message,
#                     'samsonmuoki97@gmail.com',
#                     ['samsonmuoki97@gmail.com'],
#                     fail_silently=False,
#                     html_message=f"Vehicle REG: <b>{value['RegNo']}</b> belonging to <b>{sacco.sacco_name}</b> sacco, has been reported for overspeeding at <b>{value['Speed']}</b> KM/H in this Location <a href='http://localhost:8000/reports/all/{key}'>{value['Location']}</a>."
#                 )
