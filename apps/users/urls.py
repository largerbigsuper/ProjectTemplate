from django.urls import path, include

from apps.users.drf.router import router_users

urlpatterns = [
        path('', include(router_users.urls)),
]
