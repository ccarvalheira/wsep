from django.contrib import admin

#from apps.campaign.models import Campaign
from apps.campaign.models import Dataset
from apps.campaign.models import Event
from apps.campaign.models import Campaign
from apps.campaign.models import Site



class SiteAdmin(admin.ModelAdmin):
	pass     



class CampaignAdmin(admin.ModelAdmin):
    pass




class DatasetAdmin(admin.ModelAdmin):
    
    
    list_display = ("name",
    )
    
    
     

class EventAdmin(admin.ModelAdmin):
    
    
    list_display = ("name",
    "start",
    "end",
    )
    
    
    

admin.site.register(Dataset, DatasetAdmin)

admin.site.register(Campaign, CampaignAdmin)

admin.site.register(Event, EventAdmin)

admin.site.register(Site, SiteAdmin)



