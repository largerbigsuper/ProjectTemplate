from rest_framework import routers

from apps.users import viewsets as user_viewsets
from apps.common import viewsets as common_viewsets

router_user = routers.DefaultRouter()

router_user.register('u', user_viewsets.UserViewSet, base_name='user-users')
router_user.register('checkin', user_viewsets.CheckInViewSet, base_name='user-checkin')
router_user.register('point', user_viewsets.PointViewSet, base_name='user-point')
router_user.register('area', common_viewsets.AreaViewSet, base_name='user-area')
