"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from rest_framework_swagger.views import get_swagger_view

from core.routers import ApiRouter

from core.views import LoginView, LogoutView
from forecast.views.api import ForecastViewSet, DayForecastViewSet
from realtime.views.api import LastRealtimeData

# BEGIN API
schema_view = get_swagger_view(title='TorinoMeteo REST API')
# django rest default api view
router = ApiRouter()
router.register(r'forecast/day', DayForecastViewSet, 'forecast day')
router.register(r'forecast', ForecastViewSet)
router.register(r'realtime/data', LastRealtimeData, 'last realtime data')
# END API

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # ckeditor uploader
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^realtime/', include('realtime.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^previsioni/', include('forecast.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^webcam/', include('webcam.urls')),
    url(r'^treenav/', include('treenav.urls')),
    # login / registration
    url(r'^account/', include('social_auth.urls')),

    # REST API
    url(r'^api/v1/auth/login/$', LoginView.as_view(),
        name='torinometeo-api-auth-login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(),
        name='torinometeo-api-auth-logout'),
    url(r'^api/doc/$', schema_view),
    url(r'^api/v1/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    ]
    urlpatterns += [
        url(r'^static/(?P<path>.*)$',
            'django.contrib.staticfiles.views.serve'),
    ]
