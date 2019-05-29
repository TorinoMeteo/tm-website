from rest_framework.routers import DefaultRouter
from rest_framework import views
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.urls.exceptions import NoReverseMatch

from collections import OrderedDict


class ApiRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        """
        Return a view to use as the API root.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, *args, **kwargs):
                ret = OrderedDict()
                namespace = request.resolver_match.namespace
                for key, url_name in api_root_dict.items():
                    if namespace:
                        url_name = namespace + ':' + url_name
                    try:
                        ret[key] = reverse(
                            url_name,
                            args=args,
                            kwargs=kwargs,
                            request=request,
                            format=kwargs.get('format', None)
                        )
                        if key == 'forecast':
                            ret['forecast-last'] = '%s%s' % (ret['forecast'], 'get-last/') # noqa
                    except NoReverseMatch:
                        continue

                return Response(ret)

        return APIRoot.as_view()
