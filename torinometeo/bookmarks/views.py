from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from realtime.models.stations import Station
from .models import StationBookmark


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AddStationBookmarkView(LoginRequiredMixin, View):
    def get(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        user = request.user
        bookmark, created = StationBookmark.objects.get_or_create(
            user=user,
            station=station
        )
        bookmark.save()
        return JsonResponse({'status': 'ok'})


class RemoveStationBookmarkView(LoginRequiredMixin, View):
    def get(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        user = request.user
        bookmark = StationBookmark.objects.get(
            user=user,
            station=station
        )
        bookmark.delete()
        return JsonResponse({'status': 'ok'})
