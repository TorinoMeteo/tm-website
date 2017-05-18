# encoding: utf-8
'''
Here there is the implementation of the policy login related.


 - We want to enforce the presence of the mail
 - We want an unique username

For examples look at <examples/django_example/example/app/pipeline.py>.
'''
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core import signing

from social.exceptions import AuthFailed
from social.pipeline.partial import partial

import logging

logger = logging.getLogger(__name__)

def check_details(backend, response, **kwargs):
    """ This must be placed before any pipeline in order to check
    that email-registration parameters are inserted and basic conditions validates True """
    username = response.get('username')
    email    = response.get('email')
    email2    = response.get('email2')
    password = response.get('password')
    password2 = response.get('password2')
    privacy = response.get('check_privacy')

    if backend.name == 'email' and (privacy != '1'):
        raise AuthFailed(backend, u'In order to register to our website you must accept the privacy terms and conditions')

    if backend.name == 'email' and (not username or not email):
        raise AuthFailed(backend, u'Please fill all the required fields')

    if backend.name == 'email' and (email != email2):
        raise AuthFailed(backend, u'E-mail mismatch')

    if backend.name == 'email' and (password != password2):
        raise AuthFailed(backend, u'Passwords mismatch')

    if backend.name == 'email' and User.objects.filter(username=username).exists():
        #FIXME update python-social-auth which shoiuld fix UnicodeEncodeError: 'ascii' codec can't encode character u'\\xe8' in position
        raise AuthFailed(backend, u'The username %s is not available' % username)

    if backend.name == 'email' and  User.objects.filter(email=email).exists():
        #FIXME update python-social-auth which shoiuld fix UnicodeEncodeError: 'ascii' codec can't encode character u'\\xe8' in position
        raise AuthFailed(backend, u'The e-mail address %s is already registered' % email)

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('account-require-email')

# https://github.com/omab/psa-allauth/blob/master/example/app/pipeline.py
def set_password(strategy, backend, user, response, is_new=False,
                 *args, **kwargs):

    if backend.name in ('email', 'username') and is_new and response.get('password'):
        user.set_password(response.get('password')[0])
        user.save()

def add_user_to_correct_group(strategy, backend, user, response, is_new=False, **kwargs):
    """ User registered through frontend belongs to the group settings.USERS_GROUP_NAME """
    try:
        g = Group.objects.get(name=settings.USERS_GROUP_NAME)
    except:
        g = Group.objects.create(name=settings.USERS_GROUP_NAME)
        g.save()

    user.groups.add(g)
    user.save()

# http://psa.matiasaguirre.net/docs/pipeline.html#email-validation
# https://github.com/omab/psa-allauth/blob/master/example/app/mail.py
def email_validation(strategy, backend, code):

    # force session save
    strategy.request.session.save()
    print 'DIOPORCOOOOOO'
    print strategy.session.session_key
    signature = signing.dumps({"session_key": strategy.session.session_key, "email": code.email},
                              key=settings.EMAIL_SECRET_KEY)

    url = reverse('social:complete', args=(backend.name,)) + \
            '?verification_code=' + code.code + \
            '&signature=' + signature

    url = strategy.request.build_absolute_uri(url)

    logger.info('sending verification mail to %s' % code.email)
    logger.debug('sending verification mail code: %s' % code)

    send_mail('TorinoFood - Please verify your email address',
        'In order to verify your registration, please follow this link, or copy and paste it in your browser\'s address bar::\n{0}'.format(url),
        settings.EMAIL_FROM,
        [code.email],
        fail_silently=False)
