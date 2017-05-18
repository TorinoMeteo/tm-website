from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.context_processors import csrf

class SignInView(View):
    """ SignIn view
    This view is called by ajax and its content is rendered inside a modal body
    """
    def get(self, request):
        next = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
        action = request.GET.get('action', None)
        if action and getattr(settings, 'SOCIAL_AUTH_ACTION_' + action.upper(), None):
            info = getattr(settings, 'SOCIAL_AUTH_ACTION_' + action.upper())
        else:
            info = None
        params = {'request': request, 'next': next, 'info': info}
        params.update(csrf(request))
        return render_to_response('social_auth/signin.html', params)

def mail_required(request):
    """ Error message view, the email is required
    """
    backend = request.session['partial_pipeline']['backend']
    return render_to_response('social_auth/mail_required.html', {
        'backend': backend,
    }, RequestContext(request))

def mail_sent(request):
    backend = request.session['partial_pipeline']['backend']
    return render_to_response('social_auth/mail_sent.html', {
        'backend': backend,
    }, RequestContext(request))

def check_username(request):
    available = False if User.objects.filter(username=request.GET.get('username')).count() else True
    return JsonResponse({'available': available})

