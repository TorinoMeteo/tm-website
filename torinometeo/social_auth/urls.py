from django.conf.urls import include, url
from django.contrib.auth import views
from django.views.generic.base import TemplateView

from .views import SignInView, check_username, mail_required, mail_sent

urlpatterns = [
    # login / registration
    url(r'^$', SignInView.as_view(), name='account-signin'),
    url(r'^mail-required/$', mail_required, name='account-require-email'),
    url(r'^check-username/$', check_username, name='account-check-username'),
    url(r'^errors/$',
        TemplateView.as_view(template_name='social_auth/errors.html'),
        name='account-errors'),
    url(r'^email-sent/$', mail_sent),
    url(r'^logout/$',
        views.LogoutView.as_view(),
        name='account-logout'),
    url(r'^login/$',
        views.LoginView.as_view(template_name='social_auth/login.html'),
        name='login'),
    url(r'^password_change/$',
        views.PasswordChangeView.as_view(),
        name='password_change'),
    url(r'^password_change/done/$',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    url(r'^password_reset/$',
        views.PasswordResetView.as_view(template_name='social_auth/password_reset_form.html'),
        name='password_reset'),
    url(r'^password_reset/done/$',
        views.PasswordResetDoneView.as_view(template_name='social_auth/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(template_name='social_auth/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        views.PasswordResetCompleteView.as_view(template_name='social_auth/password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'', include('social_django.urls', namespace='social'))
]
