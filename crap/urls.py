from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from apps.tracker.views import ReceiverView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', include('apps.personalization.urls')),
    path('', include('apps.tracker.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('receive/', csrf_exempt(ReceiverView.as_view())),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
