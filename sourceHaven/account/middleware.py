from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RedirectAuthenticatedUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        for_redirect = [reverse('account:login'), reverse('account:registration')]
        if request.user.is_authenticated and request.path in for_redirect:
            return redirect('account:dashboard')
