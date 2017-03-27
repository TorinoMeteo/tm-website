from django.shortcuts import render
from django.views.generic import View, DetailView, ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse

from blog.models import Entry

class EntryDetailView(DetailView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(published=True)

class CategoryListView(ListView):
    model = Entry
    template_name = 'blog/category_list.html'
    paginate_by = 5

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Entry.objects.filter(published=True, tags__name__in=[tag]).order_by('-last_edit_date')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']

        return context

class ArchiveView(ListView):
    model = Entry
    template_name = 'blog/archive_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Entry.objects.filter(published=True).order_by('-last_edit_date')
