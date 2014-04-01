from django.db import models

#class HasOwnerMixin(models.Model):
#    owner = models.Foreign


class ResearchObject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    
    
    class Meta:
        abstract = True
        pass
    
    def __unicode__(self):
        return self.name
    
    def get_object_type(self):
        return self.__class__.__name__
    


