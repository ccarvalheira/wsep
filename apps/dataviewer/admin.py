from django.contrib import admin

from apps.dataviewer.models import Aggregator
from apps.dataviewer.models import Calculator
from apps.dataviewer.models import BaseTemplate
#from apps.dataviewer.models import Dataviewer
from apps.dataviewer.models import Dimension
from apps.dataviewer.models import Filter
#from apps.dataviewer.models import Procedure
#from apps.dataviewer.models import Datatype
#from apps.dataviewer.models import Workflow

from apps.jobs.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','tasklet_count', 'done')

class AggregatorAdmin(admin.ModelAdmin):
    pass
    

class FilterAdmin(admin.ModelAdmin):
    pass
     

class CalculatorAdmin(admin.ModelAdmin):
    
    pass
    
    
     

class BaseTemplateAdmin(admin.ModelAdmin):
    
    
    list_display = ("name",
    )

    
class DimensionAdmin(admin.ModelAdmin):
    
    
    list_display = ("name",
    "units",
    "datatype",
    "ts_column",
    )
    
    
    
    
    
admin.site.register(Aggregator, AggregatorAdmin)


admin.site.register(Calculator, CalculatorAdmin)


admin.site.register(BaseTemplate, BaseTemplateAdmin)


admin.site.register(Dimension, DimensionAdmin)


admin.site.register(Filter, FilterAdmin)

admin.site.register(Task, TaskAdmin)

