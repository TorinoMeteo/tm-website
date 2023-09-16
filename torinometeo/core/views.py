from django.contrib.auth import authenticate
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from core.serializers import UserSerializer

import base64
import hmac
import hashlib
import time
import logging

logger = logging.getLogger(__name__)


class LoginView(views.APIView):
    """
    API authentication.
    Checks if the provided credentials correspond to an user associated
    with an account, in such case the user token is returned in a
    200 response.
    """

    def post(self, request, format='json'):

        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                serialized = UserSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': serialized.data
                })
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """
    User unauthentication.
    If the requests arrives from an authenticated client performs a logout
    @TODO regenerate token
    """
    def post(self, request, format='json'):
        return Response({
            'status': 'OK',
            'message': 'Logout succedeed.'
        }, status=status.HTTP_200_OK)


class PizzaGptApiView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # no need for CSRF protection since it is an HMAC request
        return super(PizzaGptApiView,
                     self).dispatch(request, *args, **kwargs)

    def post(self, request):
        bs = request.POST.get('date').encode('utf-8')
        dig = hmac.new(
            bytes(settings.API_KEY, 'latin-1'), bs,
            digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(dig).decode()

        if signature != request.POST.get('signature', None):
            return JsonResponse({'success': False}, status=401)

        question = request.POST.get('question', None)

        if question is not None:
            logger.info('Question: ' + question)
            # try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-dev-shm-usage')

            logger.info('Starting driver')

            path = '/snap/bin/chromium.chromedriver'
            driver = webdriver.Chrome(options=chrome_options, executable_path=path)

            driver.get("https://www.pizzagpt.it")

            logger.info('accept cookies')
            button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/button[1]/p')))
            logger.info('button found')
            button.click()

            logger.info('Waiting for textarea')
            textarea = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/div[4]/div/textarea')))
            textarea.send_keys(question);
            button = driver.find_element(By.XPATH, '//*[@id="send"]')
            button.click()

            logger.info('Textarea found')

            while 'Caricamento' in WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/div[3]/div[2]/div[3]/div[2]'))).text:
                time.sleep(5)

            response_text = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/div[3]/div[2]/div[3]/div[2]'))).text
            json_response = {'success': True, 'text': response_text}

            return JsonResponse(json_response, status=200)
            # except Exception as e:
                # return JsonResponse({'success': False}, status=429)

        return JsonResponse({'success': False}, status=429)
