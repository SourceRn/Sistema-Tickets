from django.http import Http404

class BloqueoAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/gestion-interna/'):
            if not request.user.is_authenticated or not request.user.is_superuser:
                raise Http404()

        return self.get_response(request)