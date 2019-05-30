from django.contrib import admin

from blog.models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'last_edit_date', 'published',
                    'featured',)
    list_filter = ['creation_date', 'last_edit_date', 'featured', ]
    list_editable = ['published', 'featured']
    prepopulated_fields = {'slug': ('title',)}


    fieldsets = (('Principale', {
        'fields': (
            'title',
            'slug',
            'text',
            'image',
            'tags',
            'index_words',
            'published',
        ),
        'classes': (
            'baton-tabs-init',
            'baton-tab-fs-flags',
        )
    }), ('Opzioni', {
        'fields': (
            'featured',
            'enable_comments',
            'related_entries',
        ),
        'classes': ('tab-fs-flags', )
    }))

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
