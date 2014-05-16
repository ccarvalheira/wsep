from django.db import models

from apps.researchobjects.models import ResearchObject

class Archive(ResearchObject):
    #file_field = models.CharField(max_length=10)
    file_field = models.FileField(upload_to="archives", help_text="")
    dataset = models.ForeignKey("campaign.Dataset", blank=True, null=True)
    campaign = models.ForeignKey("campaign.Campaign", blank=True, null=True)
    
    
    


