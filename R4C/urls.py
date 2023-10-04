from django.contrib import admin
from django.urls import include, path

from customers.urls import urlpatterns as customers_urlpatterns
from robots.urls import urlpatterns as robots_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(customers_urlpatterns)),
    path('', include(robots_urlpatterns)),
]
