from django.db import models

from django.contrib.auth.models import AbstractUser
#from provider.oath2.models import Client
#from django.contrib.auth.models import Group
from apps.researchobjects.models import ResearchObject

class WSUser(AbstractUser, ResearchObject):
    #first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, null=True, blank=True)

class Permission(models.Model):
    object_type = models.CharField(max_length=100)
    object_id = models.IntegerField()
    object_url = models.TextField()
    user = models.ForeignKey(WSUser, related_name="my_permissions")
    owner = models.ForeignKey(WSUser, related_name="owns")
    read = models.BooleanField()
    update = models.BooleanField()
    delete = models.BooleanField()


#class Comment(models.Model):
#    wsuser = models.ForeignKey("WSUser", related_name="commented")
#    researchobject = models.ForeignKey("researchobjects.ResearchObject")
#    content = models.TextField()
#    up_vote = models.ManyToManyField("WSUser", related_name="upvotes")
#    down_vote = models.ManyToManyField("WSUser", related_name="downvotes")
    
#    def __unicode__(self):
#        return self.content


