from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from tastypie import fields

from apps.campaign.models import Campaign
from apps.campaign.models import Site
from apps.campaign.models import Event
from apps.campaign.models import Dataset
from apps.campaign.models import Device

    
        

class SiteResource(ModelResource):
    class Meta:
        queryset = Site.objects.all()
        resource_name = "site"
        authorization = Authorization()
        
class CampaignResource(ModelResource):
    site = fields.ForeignKey(SiteResource, "site")
    class Meta:
        queryset = Campaign.objects.all()
        resource_name = 'campaign'
        authorization = Authorization()
        exclude = ["id"]
    
            

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = "event"
        authorization = Authorization()
        
""" Dataset metadata """
class DatasetMetaResource(ModelResource):
    class Meta:
        queryset = Dataset.objects.all()
        resource_name = "datasetmeta"
        authorization = Authorization()
        
class DeviceResource(ModelResource):
    class Meta:
        queryset = Device.objects.all()
        resource_name = "device"
        authorization = Authorization()
        



        
        
