
from django.shortcuts import render

import pyrebase

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from registration.models import Vehicle, Sacco, Driver
from reports.models import (
    # Report,
    TrackVehicleReports
)
# from .forms import ResolveCaseForm
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
