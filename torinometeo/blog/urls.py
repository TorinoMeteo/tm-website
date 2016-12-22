from django.conf.urls import patterns,url
from blog.views import EntryDetailView, CategoryListView, ArchiveView

urlpatterns = patterns('blog.views',
    url(r'^archivio/?$', ArchiveView.as_view(), name='blog-archive'),
    url(r'^categoria/(?P<tag>.+)/$', CategoryListView.as_view(), name='blog-category-list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', EntryDetailView.as_view(), name='blog-detail'),
)

