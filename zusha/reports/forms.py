from django import forms

PENDING = 'Pending'
IN_PROGRESS = 'In Progress'
RESOLVED = 'Resolved'

RESOLUTION_OPTIONS = [
    (PENDING, ('No action was taken')),
    (IN_PROGRESS, ('Currently being resolved')),
    (RESOLVED, ('Corrective Action was taken'))
]


class ResolveCaseForm(forms.Form):
    """Viewset for add driver."""
    regno = forms.CharField(max_length=8)
    sacco = forms.CharField(max_length=10)
    date_reported = forms.CharField(max_length=20)
    # date_reported = forms.DateTimeField(
    #     auto_now=False, auto_now_add=False
    # )
    # date_resolved = forms.DateTimeField(
    #     auto_now=False, auto_now_add=False
    # )
    action = forms.CharField(
        # choices=RESOLUTION_OPTIONS,
        max_length=20,
        # default=PENDING
    )
