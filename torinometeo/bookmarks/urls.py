from django.conf.urls import url

from bookmarks.views import AddStationBookmarkView, RemoveStationBookmarkView

urlpatterns = [
    url(r'^aggiungi/stazione/(?P<pk>\d+)/?$',
        AddStationBookmarkView.as_view(),
        name='bookmarks-add-station'),
    url(r'^rimuovi/stazione/(?P<pk>\d+)/?$',
        RemoveStationBookmarkView.as_view(),
        name='bookmarks-remove-station'),
]
