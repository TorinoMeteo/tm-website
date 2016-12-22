from django.contrib import admin

from blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
    fields = ['creation_date', 'last_edit_date', 'title', 'slug', 'text', 'image', 'tags', 'index_words', 'published', 'featured', 'enable_comments', 'related_entries', 'num_read', ]
    list_display = ('title', 'creation_date', 'last_edit_date', 'published', 'featured',)
    list_filter = ['creation_date', 'last_edit_date', 'featured',]
    list_editable = ['published', 'featured']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Entry, EntryAdmin)
