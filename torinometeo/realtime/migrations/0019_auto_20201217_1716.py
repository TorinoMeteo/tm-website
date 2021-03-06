# Generated by Django 2.2.1 on 2020-12-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0018_airqualitystation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='airqualitystation',
            options={'ordering': ('name',), 'verbose_name': 'stazione aria', 'verbose_name_plural': 'stazioni aria'},
        ),
        migrations.AddField(
            model_name='airqualitystation',
            name='data_url',
            field=models.URLField(default='', verbose_name='URL dati'),
            preserve_default=False,
        ),
    ]
