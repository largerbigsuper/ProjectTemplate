from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


from utils.modelmanager import ModelManager


class AreaManager(ModelManager):

    def province(self):
        return self.filter(level=0)

    def _get_children(self, pk, level):
        return self.filter(parent_id=pk, level=level)

    def citys_in_province(self, pk):
        return self._get_children(pk, level=1)

    def towns_in_city(self, pk):
        return self._get_children(pk, level=2)


class Area(MPTTModel):
    code = models.CharField(verbose_name='编码', max_length=100, unique=True)
    name = models.CharField(verbose_name='名称', max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    objects = AreaManager()

    class Meta:
        db_table = 'area'
        verbose_name = verbose_name_plural = '省/市/地区(县)'
    
    def __str__(self):
        return self.name


mm_Area = Area.objects
