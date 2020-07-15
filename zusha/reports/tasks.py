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

from registrations.models import (
    Sacco,
    RegisteredDriver,
    SaccoDriver,
    Vehicle
)
from .models import (
    SpeedingInstance, DailyVehicleReport, DailySaccoReport, DailyDriverReport
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
        day = date(
            int(date_list[0]), int(date_list[1]), int(date_list[2])
        )
        SpeedingInstance.objects.get_or_create(
            regno=regno,
            sacco=sacco,
            speed=speed,
            time=time,
            location=location,
            date=day
        )


@shared_task
def track_each_vehicle_reports():
    reports = SpeedingInstance.objects.all()
    for report in reports:
        case_count = SpeedingInstance.objects.filter(
            regno=report.regno, date=report.date
        ).count()
        tracker, created = DailyVehicleReport.objects.get_or_create(
            regno=report.regno,
            date=report.date,
            sacco=report.sacco,
            defaults={'count': case_count},
        )


@shared_task
def track_each_sacco_reports():
    reports = SpeedingInstance.objects.all()
    for report in reports:
        case_count = SpeedingInstance.objects.filter(
            sacco=report.sacco, date=report.date
        ).count()
        tracker, created = DailySaccoReport.objects.get_or_create(
            sacco=report.sacco,
            date=report.date,
            defaults={'count': case_count},
        )


@shared_task
def track_each_driver_reports():
    reports = SpeedingInstance.objects.all()
    for report in reports:
        case_count = SpeedingInstance.objects.filter(
            driver=report.driver, date=report.date, regno=report.regno
        ).count()
        tracker, created = DailyDriverReport.objects.get_or_create(
            driver=report.driver,
            sacco=report.sacco,
            regno=report.regno,
            date=report.date,
            defaults={'count': case_count},
        )


@shared_task
def blacklist_saccos():
    saccos = Sacco.objects.all()
    reports = DailyVehicleReport.objects.filter(
        # ntsa_action="Pending"
        ntsa_action="Pending"
    )
    # import pdb
    # pdb.set_trace()
    for sacco in saccos:
        reports_list = []
        for report in reports:
            # if report.sacco == sacco.sacco_name:
            if report.sacco == sacco.sacco_name and report.date > sacco.last_inspection_date:
                reports_list.append(report)
        if len(reports_list) > 0:
            sacco.license_status = "Blacklisted"
            sacco.save()


@shared_task
def blacklist_vehicles():
    vehicles = Vehicle.objects.all()
    reports = SpeedingInstance.objects.all()
    for vehicle in vehicles:
        reports_list = []
        for report in reports:
            if report.regno == vehicle.registration_number:
                reports_list.append(report)
        if len(reports_list) > 5:
            vehicle.license_status = "Blacklisted"
            vehicle.save()


utc = pytz.utc


# TODO optimise driver reporting
@shared_task
def blacklist_drivers():
    # drivers = SaccoDriver.objects.all()
    # reports = SpeedingInstance.objects.all()
    # daily_reports = DailyVehicleReport.objects.filter(
    #     ntsa_action="Pending"
    # )
    # for driver in drivers:
    #     reports_list = []
    #     for report in reports:
    #         if report.driver_id == driver.driver_id:
    #             reports_list.append(report)
    #     if len(reports_list) > 1:
    #         driver.license_status = "BLACKLISTED"
    #         driver.save()
    drivers = RegisteredDriver.objects.all()
    reports = DailyDriverReport.objects.filter(
        ntsa_action="Pending"
    )
    for driver in drivers:
        reports_list = []
        for report in reports:
            # if report.driver == driver.driver:
            if report.driver == driver.driver and report.date > driver.last_revision_date:
                reports_list.append(report)
        if len(reports_list) > 1:
            driver.license_status = "Blacklisted"
            driver.save()
