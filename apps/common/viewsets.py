from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.pagination import ReturnAllPagination
from .serializers import AreaSerializer
from .models import mm_Area


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    
    permission_classes = []
    serializer_class = AreaSerializer
    queryset = mm_Area.all().order_by('parent_id')
    pagination_class = ReturnAllPagination

    def get_queryset(self):
        if self.action in ['list', 'province']:
            return mm_Area.province()
        else:
            return mm_Area.all().order_by('parent_id')

    @action(detail=False)
    def province(self, request):
        """所有省份列表
        """
        self.queryset = mm_Area.province()
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(data=serializer.data)

    @action(detail=True)
    def citys(self, request, pk=None):
        """某个省所有的市列表
        """
        self.queryset = mm_Area.citys_in_province(pk)
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(data=serializer.data)

    @action(detail=True)
    def towns(self, request, pk=None):
        """某个市所有的县列表
        """
        self.queryset = mm_Area.towns_in_city(pk)
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(data=serializer.data)
