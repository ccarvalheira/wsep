from django.db import models

from apps.researchobjects.models import ResearchObject
from apps.dataviewer.models import Calculator


class Campaign(ResearchObject):
    """ Catchall grouping of Datasets. The BL may use this to group Datasets as they desire. """
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True,)
    site = models.ForeignKey("Site",blank=True,null=True,)
    #owner = models.ForeignKey("wsusers.WSUser")
  
    
    def __unicode__(self):
        return self.name

#register(["read","write"],Campaign, "apps.campaign")

    
class Site(ResearchObject):
    """ Geographic site. A MeasurementSet may or may not be associated with a Site """
    location = models.CharField(blank=True,null=True,max_length=100,)
    
    def __unicode__(self):
        return self.name
    
class Event(ResearchObject):
    """ A generic object that records an event that hapened related to a given MeasurementSet """
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    campaign = models.ForeignKey("Campaign",)
    
    def __unicode__(self):
        return self.name
    
class Dataset(ResearchObject):
    """ The blueprint for the incoming time series data. """
    campaign = models.ForeignKey("Campaign")
    dimensions = models.ManyToManyField("dataviewer.Dimension")
    highest_ts = models.CharField(max_length=50, blank=True, null=True)
    lowest_ts = models.CharField(max_length=50, blank=True, null=True)
    devices = models.ManyToManyField("Device")
    datapoint_count = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    
    datapoints_per_bucket = 10000
    
    def __unicode__(self):
        return self.name
    
    def get_columns(self):
        base_columns = self.get_base_columns()
        calc_columns = [c.output_dimension.cassandra_column for c in Calculator.objects.filter(procedure_ptr__dataviewer__dataset=self)]
        return base_columns + calc_columns
    
    def get_base_columns(self):
        return [d.cassandra_column for d in self.template.dimensions.exclude(cassandra_column="id")]
    
    def get_bucket_list(self):
        return ["'"+str(self.id)+"-"+str(c)+"'" for c in xrange(1+(self.datapoint_count/self.datapoints_per_bucket))]
        
    def get_str_bucket_list(self):
        return ",".join(self.get_bucket_list())


class Device(ResearchObject):
    pass
    
    
