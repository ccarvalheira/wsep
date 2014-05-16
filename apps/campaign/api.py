from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL

from apps.campaign.models import Campaign
from apps.campaign.models import Site
from apps.campaign.models import Event
from apps.campaign.models import Dataset
from apps.campaign.models import Device

from apps.dataviewer.models import Dimension

from apps.wsadmin.models import CassandraNode

from cassandra.cluster import Cluster

####
""" We define this here so SiteResource can use it. The real definition is below. """
class CampaignResource(ModelResource):
    class Meta:
        queryset = Campaign.objects.all()
        resource_name = 'campaign'
        authorization = Authorization()
####


class SiteResource(ModelResource):
    """ Geographic site in which Campaigns are carried out. """
    campaigns = fields.ToManyField(CampaignResource, "campaign_set", null=True, blank=True)
    class Meta:
        queryset = Site.objects.all()
        resource_name = "site"
        authorization = Authorization()
        

""" Real definition of CampaignResource. """
class CampaignResource(ModelResource):
    """ A Campaign that is carried out in a Site and has a number of related Datasets. """
    site = fields.ForeignKey(SiteResource, "site", null=True, blank=True)
    class Meta:
        queryset = Campaign.objects.all()
        resource_name = 'campaign'
        authorization = Authorization()
    
            

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = "event"
        authorization = Authorization()
        

class DeviceResource(ModelResource):
    class Meta:
        queryset = Device.objects.all()
        resource_name = "device"
        authorization = Authorization()
        

""" Dataset metadata """
class DatasetMetaResource(ModelResource):
    #devices = fields.ToManyField(DeviceResource, "devices", null=True, blank=True)
    campaign = fields.ToOneField(CampaignResource, "campaign")
    site = fields.ToOneField(SiteResource,"campaign__site", null=True, blank=True)
    dimensions = fields.ToManyField("apps.dataviewer.api.DimensionResource", "dimensions")
    datapoint_count = fields.IntegerField("datapoint_count")
    
    class Meta:
        queryset = Dataset.objects.all()
        resource_name = "dataset"
        authorization = Authorization()
        
        #excludes = ["highest_ts", "lowest_ts"]
        
        filtering = {"site": ALL}
        
        
    
    def obj_create(self, bundle, **kwargs):
        
        from apps.dataviewer.api import DimensionResource

        bundle.obj = Dataset()
        bundle = self.full_hydrate(bundle)
        bundle.obj.save()
        
        for d in bundle.data["dimensions"]:
            bundle.obj.dimensions.add(DimensionResource().get_via_uri(d, bundle.request))
            bundle.obj.save()
    
        bundle.obj.dimensions.add(Dimension.objects.get(ts_column="time"))
        
        bundle.obj.save()
        
        return bundle.obj
    
    def get_detail(self, request, **kwargs):
        """
        Returns a single serialized resource.

        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        basic_bundle = self.build_bundle(request=request)

        try:
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        #inserted here to display the datapoints for this particular dataset
        bundle = self.dehydrant_detail(bundle)
        ###
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)
    
    def hydrate(self, bundle):
        bundle.data["upper_time"] = "'123'"
        return bundle
    
    def dehydrant_detail(self, bundle):
        """ Lists the datapoints for the given object. """
        columns = ",".join([b.ts_column.lower() for b in bundle.obj.dimensions.all()])
        
        try:
            upper_time = "'"+bundle.request.GET["upper_time"]+"'"
        except KeyError:
            upper_time = "'99999'"
        
        try:
            lower_time = "'"+bundle.request.GET["lower_time"]+"'"
        except KeyError:
            lower_time = "'1'"
        
        stmt = "select %s, dataset, bucket from tsstore where dataset=%s and bucket in (%s) and time >= %s and time < %s order by dataset, time;" % (columns, bundle.obj.id, bundle.obj.get_str_bucket_list(), lower_time, upper_time)
        
        node_list = CassandraNode.get_nodeip_list()
        cluster = Cluster(node_list)
        session = cluster.connect('ws')
        
        datapoints = session.execute(stmt)
        
        session.shutdown()
        rows = []
        for d in datapoints:
            dic = {}
            for col in [(b.ts_column.lower(), b.name) for b in bundle.obj.dimensions.all()]:
                dic[col[1]] = d.__dict__[col[0]]
            rows.append(dic)
            
        bundle.data["datapoints"] = rows
        return bundle
   
    
    def obj_get_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get_list``.

        Takes an optional ``request`` object, whose ``GET`` dictionary can be
        used to narrow the query.
        """
        filters = {}

        if hasattr(bundle.request, 'GET'):
            # Grab a mutable copy.
            filters = bundle.request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)
        
        # transform input data "site" from uri to object for filtering
        try:
            site_uri = filters["site"]
            site_obj = SiteResource().get_via_uri(site_uri)
            filters["site"] = str(site_obj.id)
        except KeyError:
            pass
        ###
        applicable_filters = self.build_filters(filters=filters)

        try:
            objects = self.apply_filters(bundle.request, applicable_filters)
            return self.authorized_read_list(objects, bundle)
        except ValueError:
            raise BadRequest("Invalid resource lookup data provided (mismatched type).")
              

class DeviceResource(ModelResource):
    datasets = fields.ManyToManyField(DatasetMetaResource, "dataset_set", null=True)
    class Meta:
        queryset = Device.objects.all()
        resource_name = "device"
        authorization = Authorization()
        
        

