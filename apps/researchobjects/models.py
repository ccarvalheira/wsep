from django.db import models

#class HasOwnerMixin(models.Model):
#    owner = models.Foreign


class ResearchObject(models.Model):
    name = models.CharField(max_length=100, help_text="Unicode string data. The name of this resource.")
    description = models.TextField(blank=True, null=True, help_text="Unicode string data. A human readable description of this resource.")
    metadata = models.TextField(blank=True, null=True, help_text="Unicode string data. Machine readable metadata (JSON, for example) about this resource.")
    
    
    class Meta:
        abstract = True
        pass
    
    def __unicode__(self):
        return self.name
    
    def get_object_type(self):
        return self.__class__.__name__
    


