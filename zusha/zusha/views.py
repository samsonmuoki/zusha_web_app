
from django.shortcuts import render

import pyrebase

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from registration.models import Vehicle, Sacco, Driver
from reports.models import Report
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
