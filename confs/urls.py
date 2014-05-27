from django.conf.urls import patterns, include, url

#from apps.campaign.views import CenasView


from apps.wsusers.api import PermissionResource
from apps.wsusers.api import WSUserResource

from apps.campaign.api import CampaignResource
from apps.campaign.api import SiteResource
from apps.campaign.api import EventResource
from apps.campaign.api import DatasetMetaResource
from apps.campaign.api import DeviceResource

from apps.archives.api import ArchiveResource

from apps.dataviewer.api import DimensionResource
from apps.dataviewer.api import DatapointResource
from apps.dataviewer.api import BaseTemplateResource
from apps.dataviewer.api import AggregatorResource
from apps.dataviewer.api import CalculatorResource
from apps.dataviewer.api import FilterResource

from apps.tripleapi.api import GraphResource
from apps.tripleapi.api import TripleResource
from apps.tripleapi.api import LiteralStatementResource

from apps.jobs.api import TaskResource
from apps.jobs.api import TaskUpdateResource
#from apps.jobs.api import OrderedTaskResource


from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(WSUserResource())
v1_api.register(PermissionResource())

v1_api.register(CampaignResource())
v1_api.register(SiteResource())
v1_api.register(EventResource())
v1_api.register(DatasetMetaResource())
v1_api.register(DeviceResource())

v1_api.register(ArchiveResource())

v1_api.register(DimensionResource())
#v1_api.register(BaseTemplateResource())
v1_api.register(AggregatorResource())
v1_api.register(CalculatorResource())
v1_api.register(FilterResource())
v1_api.register(DatapointResource())

v1_api.register(GraphResource())
v1_api.register(TripleResource())
#v1_api.register(LiteralStatementResource())

v1_api.register(TaskResource())
v1_api.register(TaskUpdateResource())
#v1_api.register(OrderedTaskResource())



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    
    #url(r'^campaign/', include('apps.campaign.urls')),
    
    #url(r'^archives/', include('apps.archives.urls')),
    
    #url(r'^dataviewer/', include('apps.dataviewer.urls')),
    
    (r'^api/', include(v1_api.urls)),
    
    #url(r'^api/v1.0/', include('apps.apiv1.urls')),
    
    url(r'^admindoc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    #url(r'^upload/$', "apps.archives.api.upload_file"),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^task_counter/', 'apps.jobs.views.task_counter')
    
    #url(r'^docs/', include('rest_framework_swagger.urls')),

    #url(r'^/$', CenasView.as_view()),
    
)
