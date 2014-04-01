from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from apps.dataviewer.models import Dimension
from apps.dataviewer.models import BaseTemplate
from apps.dataviewer.models import Aggregator
from apps.dataviewer.models import Calculator
from apps.dataviewer.models import Filter



class DimensionResource(ModelResource):
    class Meta:
        queryset = Dimension.objects.all()
        resource_name = 'dimension'
        authorization = Authorization()


class BaseTemplateResource(ModelResource):
    class Meta:
        queryset = BaseTemplate.objects.all()
        resource_name = 'basetemplate'
        authorization = Authorization()


class AggregatorResource(ModelResource):
    class Meta:
        queryset = Aggregator.objects.all()
        resource_name = 'aggregator'
        authorization = Authorization()



class CalculatorResource(ModelResource):
    class Meta:
        queryset = Calculator.objects.all()
        resource_name = 'calculator'
        authorization = Authorization()

class FilterResource(ModelResource):
    class Meta:
        queryset = Filter.objects.all()
        resource_name = 'filter'
        authorization = Authorization()

