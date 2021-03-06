from django.db import models

from apps.researchobjects.models import ResearchObject

CASSANDRA_DATATYPE_CHOICES = (
    ("decimal","Decimal"),
    ("double","Double"),
    ("text","Array"),
    ("text","Text"),
)



class Dimension(ResearchObject):
    units = models.CharField(max_length=20, help_text="Unicode string. The units of measurement of this dimension (ex: Bar, C).")
    datatype = models.CharField(max_length=10, choices=CASSANDRA_DATATYPE_CHOICES, help_text="Datatype of this dimension. May be "+str([choice[1] for choice in CASSANDRA_DATATYPE_CHOICES]))
    ts_column = models.CharField(max_length=50, help_text="Name of the column in cassandra. I don't think this should be exposed in the API.")
    
    
    def __unicode__(self):
        return self.name + " - " + self.datatype
    
    def format_column(self):
        return self.ts_column + " " + self.datatype
    
class BaseTemplate(ResearchObject):
    dimensions = models.ManyToManyField("Dimension",)
    
    def __unicode__(self):
        return self.name
    
    def get_tablename(self, agg=False):
        if not agg:
            tablename = self.name.strip().replace(" ","").lower()
        else:
            tablename = self.name.strip().replace(" ","").lower()+"_agg"
        return tablename
        
    def get_create_str(self, agg=False):
        column_list = self.dimensions.exclude(name="id")
        formatted_columns = ",".join([c.format_column() for c in column_list])
        tablename = self.get_tablename(agg)
        
        return "create table %s (bucket bigint, time timeuuid, dataset int, %s, primary key (bucket, dataset, time));" % (tablename, formatted_columns)
        
        
    
class Procedure(ResearchObject):
    async_function = models.CharField(max_length=100, help_text="Unicode string. The name of the asynchronous function that is used by this procedure.")
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name + " - " + self.async_function
    
    
class Aggregator(Procedure):
    interval_in_seconds = models.IntegerField(default=2, help_text="Integer. The interval, in seconds, with which to aggregate.")
    

class Calculator(Procedure):    
    output_dimension = models.ForeignKey("Dimension", related_name="output")
    input_dimensions = models.ManyToManyField("Dimension", related_name="inputs")
    #is_standard = models.BooleanField()
    custom_code = models.TextField(blank=True, null=True)
    #is_flagged = models.BooleanField()
    
    def get_create_str(self):
        return self.output_dimension.ts_column + " " + self.output_dimension.datatype

   
class Filter(Procedure):
    input_dimensions = models.ManyToManyField("Dimension")
    
