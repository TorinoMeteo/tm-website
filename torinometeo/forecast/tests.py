import datetime

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class ForecastViewsetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='tmforecast')
        permission_add = Permission.objects.get(codename='add_forecast')
        permission_change = Permission.objects.get(codename='change_forecast')
        self.user.user_permissions.add(permission_add)
        self.user.user_permissions.add(permission_change)
        self.no_perm_user = User.objects.create(username='noperm')


    def test_post_from_non_authenticated_users_gives_401(self):
        """
        """
        response = self.client.post('/api/v1/forecast/', {}, content_type='application/json') # blank data dictionary
        self.assertEqual(response.status_code, 401)

    def test_put_from_non_authenticated_users_gives_401(self):
        """
        """
        response = self.client.put('/api/v1/forecast/', {}, content_type='application/json') # blank data dictionary
        self.assertEqual(response.status_code, 401)

    def test_delete_from_non_authenticated_users_gives_401(self):
        """
        """
        response = self.client.delete('/api/v1/forecast/', {}, content_type='application/json') # blank data dictionary
        self.assertEqual(response.status_code, 401)

    def test_post_from_non_perm_users_gives_403(self):
        client = APIClient()
        token = Token.objects.get(user__username='noperm')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/api/v1/forecast/', {}, content_type='application/json') # blank data dictionary
        self.assertEqual(response.status_code, 403)

    def test_post_bad_data_from_perm_users_gives_400(self):
        client = APIClient()
        token = Token.objects.get(user__username='tmforecast')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/api/v1/forecast/', {'date': 'STOCAZZO', 'pattern': 'meow'}, format='json') # blank data dictionary
        self.assertEqual(response.status_code, 400)

    def test_post_from_perm_users_gives_201(self):
        client = APIClient()
        token = Token.objects.get(user__username='tmforecast')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/api/v1/forecast/', {'date': '2015-06-10', 'pattern': 'meow'}, format='json') # blank data dictionary
        self.assertEqual(response.status_code, 201)

