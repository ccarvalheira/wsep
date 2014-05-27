from copy import deepcopy

from tastypie.resources import ModelResource
from tastypie.resources import Resource
from tastypie.resources import fields
from tastypie.authorization import Authorization

from apps.dataviewer.models import Dimension
from apps.dataviewer.models import BaseTemplate
from apps.dataviewer.models import Aggregator
from apps.dataviewer.models import Calculator
from apps.dataviewer.models import Filter

from apps.wsadmin.models import CassandraNode

from apps.campaign.api import DatasetMetaResource


from apps.dataviewer.models import CASSANDRA_DATATYPE_CHOICES

import time
import random
import string

from cassandra.cluster import Cluster

from django_statsd.clients import statsd


class DimensionResource(ModelResource):
    class Meta:
        queryset = Dimension.objects.all()
        resource_name = 'dimension'
        authorization = Authorization()
        #excludes = ["ts_column",]
    
    def hydrate_ts_column(self,bundle):
        bundle.data.pop("ts_column",None)
        return bundle
    
    def obj_create(self, bundle, **kwargs):
        bundle.obj = Dimension()
        bundle = self.full_hydrate(bundle)
        
        valid_choices = set([c[1] for c in CASSANDRA_DATATYPE_CHOICES])
            
        if not bundle.obj.datatype in valid_choices:
            raise Exception("Invalid datatype choice. Valid choices are %s" % (str(valid_choices),))
        
        for c in CASSANDRA_DATATYPE_CHOICES:
            if c[1] == bundle.obj.datatype:
                bundle.obj.datatype = c[0]
                break        
        
        #bundle.obj.save()
        #bundle.obj.ts_column = "c"+str(bundle.obj.id)
        bundle.obj.ts_column = bundle.obj.name.lower()
        bundle.obj.save()
        
        stmt = "alter table tsstore add %s %s;" % (bundle.obj.ts_column, bundle.obj.datatype)
        node_list = CassandraNode.get_nodeip_list()
        cluster = Cluster(node_list)
        session = cluster.connect('ws')
        session.execute(stmt)
        session.shutdown()
        
        return bundle.obj


class DatapointResource(Resource):
    dataset = fields.ToOneField("apps.campaign.api.DatasetMetaResource", "dataset")
    dimensions = fields.DictField("dimensions")
    update = fields.BooleanField(null=True, blank=True)
    class Meta:
        allowed_methods = ["post", "patch", "put"]
        resource_name = "datapoint"
    
    
    def obj_create(self, bundle):
        dataset = bundle.data["dataset"]
        input_dims = [b for b in bundle.data["dimensions"]]
        
        
        dset = DatasetMetaResource().get_via_uri(dataset, bundle.request)
        dset_dims = dset.dimensions.all()
        
        idim_l = []
        for idim in input_dims:
            idd = DimensionResource().get_via_uri(idim, bundle.request)
            idd.input_value = bundle.data["dimensions"][idim]
            idim_l.append(idd)
        
        
        #for d in idim_l:
        #    if d not in dset_dims:
        #        raise Exception("invalid input dim")
        
        #for d in dset_dims:
        #    if d not in idim_l:
        #        raise Exception("not enough input dims")
        node_list = CassandraNode.get_nodeip_list()
        try:
            cluster = Cluster(node_list)
        except Exception:
            time.sleep(1)
            cluster = Cluster(node_list)
        session = cluster.connect('ws')
        columns = ",".join([str(i.ts_column) for i in idim_l])
        values = ",".join([str(i.input_value) for i in idim_l])
        bucket = dset.get_bucket_list()[-1]

        futures = []
        
        stmt = "insert into tsstore (bucket,dataset, %s) values (%s, %s, %s)" % (columns, bucket, dset.id, values)
        #raise Exception(stmt)
        fut = session.execute_async(stmt)
        futures.append(fut)
        try:
            is_update = bundle.data["update"]
        except KeyError:
            is_update = False
        if False:
            for dim in idim_l:
                if dim.ts_column == "time":
                    if not dset.highest_ts or dset.highest_ts > dim.input_value:
                        dset.highest_ts = dim.input_value.strip("'")
                        dset.save()
                    if not dset.lowest_ts or dset.lowest_ts < dim.input_value:
                        dset.lowest_ts = dim.input_value.strip("'")
                        dset.save()
                    break
        if not is_update:
            dset.datapoint_count += 1
            dset.save()
        #raise Exception(futures)
        for future in futures:
            future.result()
        session.shutdown()
        statsd.gauge("test_signal",random.choice(range(20)))

        
    
class BaseTemplateResource(ModelResource):
    class Meta:
        queryset = BaseTemplate.objects.all()
        resource_name = 'basetemplate'
        authorization = Authorization()


class AggregatorResource(ModelResource):
    class Meta:
        queryset = Aggregator.objects.all()
        resource_name = 'aggregator'
        authorization = Authorization()


class CalculatorResource(ModelResource):
    output_dimension = fields.ToOneField(DimensionResource, "output_dimension")
    input_dimensions = fields.ToManyField(DimensionResource, "input_dimensions")
    class Meta:
        queryset = Calculator.objects.all()
        resource_name = 'calculator'
        authorization = Authorization()

class FilterResource(ModelResource):
    class Meta:
        queryset = Filter.objects.all()
        resource_name = 'filter'
        authorization = Authorization()

