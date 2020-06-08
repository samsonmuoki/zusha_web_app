from django.urls import path

from . import views


app_name = 'authentications'


urlpatterns = [
    # path(
    #     'sacco_admin_signup',
    #     views.sacco_admin_signup,
    #     name="signup_sacco_admin"
    # ),
    path(
        'sacco_login/',
        views.login_sacco_admin,
        name="login_sacco_admin"
    ),

]
