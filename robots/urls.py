from django.urls import path

from .views import robots_view

urlpatterns = [
    path('robots/', robots_view, name='robots',),
]
