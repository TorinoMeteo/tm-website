# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import blog.models
import ckeditor.fields
import taggit.managers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name=b'creazione')),
                ('last_edit_date', models.DateTimeField(auto_now=True, verbose_name=b'ultima modifica')),
                ('title', models.CharField(max_length=128, verbose_name=b'titolo')),
                ('slug', models.SlugField(max_length=128, verbose_name=b'slug')),
                ('text', ckeditor.fields.RichTextField(verbose_name=b'testo')),
                ('image', models.ImageField(upload_to=blog.models.set_entry_image_folder, null=True, verbose_name=b'immagine', blank=True)),
                ('index_words', models.IntegerField(verbose_name=b'numero parole home')),
                ('published', models.BooleanField(default=False, verbose_name=b'pubblicato')),
                ('enable_comments', models.BooleanField(default=True, verbose_name=b'abilita commenti')),
                ('featured', models.BooleanField(default=False, verbose_name=b'featured')),
                ('num_read', models.IntegerField(default=0, verbose_name=b'numero letture', blank=True)),
                ('author', models.ForeignKey(related_name='entries', verbose_name=b'autore', to=settings.AUTH_USER_MODEL)),
                ('related_entries', models.ManyToManyField(related_name='_related_entries_+', null=True, verbose_name=b'articoli correlati', to='blog.Entry', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=b'valori separati da virgole', verbose_name=b'tag')),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'articolo',
                'verbose_name_plural': 'articoli',
            },
        ),
    ]
