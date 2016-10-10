from django import forms
from django.core.mail import send_mail
from django.conf import settings

from captcha.fields import CaptchaField

from realtime.models.stations import NetRequest

class NetRequestForm(forms.ModelForm):
    """ Net entrance request form
    """
    captcha = CaptchaField()
    class Meta:
        model = NetRequest
        fields = '__all__'
        widgets = {
                'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Mario', 'required': 'required', }),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Rossi', 'required': 'required', }),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'es. mario@rossi.it', 'required': 'required', }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. 011 324355',}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Via Torino Meteo 23', 'required': 'required', }),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Giaveno', 'required': 'required', }),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. TO', 'required': 'required', }),
            'nation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Italia', 'required': 'required', }),
            'lat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. 45.76443', 'required': 'required', }),
            'lng': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. 7.0453', 'required': 'required', }),
            'elevation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. 520', 'required': 'required', }),
            'station_description': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', }),
            'climate': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', }),
            'web_site_url': forms.TextInput(attrs={'type': 'url', 'class': 'form-control', 'placeholder': 'es. http://www.example.com'}),
            'webcam_url': forms.TextInput(attrs={'type': 'url', 'class': 'form-control', 'placeholder': 'es. http://www.example.com'}),
            'mean_year_rain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. 990', 'required': 'required', }),
            'station_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Davis Vantage PRO', 'required': 'required', }),
            'software_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Weewx', 'required': 'required', }),
            'installation_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. urbana, [semiurbana, extra-urbana etc..]', 'required': 'required', }),
            'installation_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. tetto, [giardino etc..]', 'required': 'required', }),
            'elevation_ground': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. 2,20', 'required': 'required', }),
            'image': forms.FileInput(attrs={'class': 'form-control', 'required': 'required', }),
        }

    def send_request_mail(self):
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        city = self.cleaned_data['city']
        send_mail('Richiesta ingresso nella rete %s %s (%s)' % (firstname, lastname, city), 'Un nuovo utente ha richiesto di entrare a far parte della rete Realtime. Accedi all\'area amministrativa per visualizzare tutte le informazioni', settings.NOREPLY_EMAIL, [settings.NET_REQUEST_EMAIL], fail_silently=False)
