from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from django.views.generic.base import TemplateView
from django.contrib.auth import views

from .views import SignInView, mail_required, mail_sent, check_username

urlpatterns = patterns('social_auth.views',

    # login / registration
    url(r'^$', SignInView.as_view(), name='account-signin'),
    url(r'^mail-required/$', mail_required, name='account-require-email'),
    url(r'^check-username/$', check_username, name='account-check-username'),
    url(r'^errors/$', TemplateView.as_view(template_name='social_auth/errors.html'), name='account-errors'),
    url(r'^email-sent/$', mail_sent),
    url(r'^logout/$', logout, {'next_page': '/'}, name='account-logout'),
    url(r'^login/$', views.login, {'template_name': 'social_auth/login.html'}, name='login'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, {'template_name': 'social_auth/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, {'template_name': 'social_auth/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, {'template_name': 'social_auth/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, {'template_name': 'social_auth/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
)
