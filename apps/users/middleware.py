from django.contrib.auth import logout
from django.http import HttpResponseRedirect


class TenantUserRedirectMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_superuser:
            if request.user.is_authenticated:
                if request.user.tenant != request.tenant:
                    return HttpResponseRedirect('//' + request.user.tenant.get_primary_domain().domain + ':8000/login/')
        response = self.get_response(request)
        return response
