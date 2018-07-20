from django.http import HttpResponse
from django.views import View


class ListToggle(View):
    def post(self, request):
        return HttpResponse()
