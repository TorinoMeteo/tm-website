from django.conf.urls import url

from blog.views import ArchiveView, CategoryListView, EntryDetailView

urlpatterns = [
    url(r'^archivio/?$', ArchiveView.as_view(), name='blog-archive'),
    url(r'^categoria/(?P<tag>.+)/$',
        CategoryListView.as_view(),
        name='blog-category-list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EntryDetailView.as_view(),
        name='blog-detail'),
]
