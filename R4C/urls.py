from django.contrib import admin
from django.urls import include, path

from robots.urls import urlpatterns as robots_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(robots_urlpatterns))
]
