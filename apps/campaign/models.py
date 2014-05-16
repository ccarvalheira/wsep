from django.db import models

from apps.researchobjects.models import ResearchObject
from apps.dataviewer.models import Calculator


class Campaign(ResearchObject):
    """ Catchall grouping of Datasets. The BL may use this to group Datasets as they desire. """
    start_date = models.DateField(blank=True, null=True, help_text="Date. Start date of this campaign.")
    end_date = models.DateField(blank=True,null=True, help_text="Date. End date of this campaign.")
    site = models.ForeignKey("Site",blank=True,null=True,)
    #owner = models.ForeignKey("wsusers.WSUser")
  
    
    def __unicode__(self):
        return self.name

#register(["read","write"],Campaign, "apps.campaign")

    
class Site(ResearchObject):
    """ Geographic site. """
    location = models.CharField(blank=True,null=True,max_length=100,help_text="Unicode string data. The location of the Site.")
    
    def __unicode__(self):
        return self.name
    
class Event(ResearchObject):
    """ A generic object that records an event that happened related to a given Campaign """
    start = models.DateTimeField(blank=True, null=True, help_text="Datetime. Start datetime for this event.")
    end = models.DateTimeField(blank=True, null=True, help_text="Datetime. End datetime for this event.")
    campaign = models.ForeignKey("Campaign",)
    
    def __unicode__(self):
        return self.name
    
class Dataset(ResearchObject):
    """ The blueprint for the incoming time series data. """
    campaign = models.ForeignKey("Campaign")
    dimensions = models.ManyToManyField("dataviewer.Dimension")
    highest_ts = models.CharField(max_length=50, blank=True, null=True, help_text="Unicode string data. Upper timestamp bound from which to filter this dataset.")
    lowest_ts = models.CharField(max_length=50, blank=True, null=True, help_text="Unicode string data. Lower timestamp bound from which to filter this dataset.")
    devices = models.ManyToManyField("Device")
    datapoint_count = models.PositiveIntegerField(default=0, help_text="Positive integer. Datapoint count for this particular dataset.")
    published = models.BooleanField(default=False, help_text="Boolean. Whether this dataset is published or not.")
    
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
    
    
