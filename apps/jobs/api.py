from django.forms import ModelForm

from tastypie.resources import ModelResource, Resource
from tastypie.authorization import Authorization

from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie.validation import FormValidation
from tastypie.bundle import Bundle

from apps.jobs.models import Task

from apps.dataviewer.api import AggregatorResource
from apps.dataviewer.api import FilterResource
from apps.dataviewer.api import CalculatorResource

from apps.dataviewer.models import Calculator

from apps.campaign.api import DatasetMetaResource

from apps.wsadmin.models import CassandraNode
from apps.wsadmin.models import GearmanNode

from gearman import GearmanClient
import pickle

class TaskUpdateResource(Resource):
    class Meta:
        resource_name = "task_update"    
        allowed_methods = ["post"]
    
    def obj_create(self, bundle, **kwargs):
        #raise Exception(bundle.data)
        obj = Task.objects.get(id=bundle.data["id"])
        try:
            obj.tasklet_count += bundle.data["increment"]
        except KeyError:
            try:
                obj.tasklet_count -= bundle.data["decrement"]
            except KeyError:
                pass
        if obj.tasklet_count < 0:
            obj.tasklet_count = 0
        obj.save()
        
        if obj.tasklet_count == 0:
            obj.done = True
            obj.save()
            try:
                new_task = obj.task_set.all()[0]
                new_dataset = DatasetMetaResource().get_via_uri(new_task.output_dataset, bundle.request)
                old_dataset = DatasetMetaResource().get_via_uri(new_task.input_dataset, bundle.request)
                new_dataset.highest_ts = old_dataset.highest_ts
                new_dataset.lowest_ts = old_dataset.lowest_ts
                new_dataset.save()
                
                
            except IndexError:
                #no more tasks to schedule
                return
            dat = {}
            dat["task"] = new_task.procedure_url
            dat["task_id"] = new_task.id
            dat["output_dataset"] = new_task.output_dataset
            dat["input_dataset"] = new_task.input_dataset
            dat["cassandra_nodes"] = CassandraNode.get_nodeip_list()
            client = GearmanClient(GearmanNode.get_nodeip_list())
            client.submit_job("pre_schedule", pickle.dumps(dat),background=True) 
            
            
            
class TaskResource(Resource):
    ordered_tasks = fields.ListField("ordered_tasks", blank=True, null=True)
    input_dataset = fields.ToOneField("apps.campaign.api.DatasetMetaResource", "input_dataset", blank=True, null=True)
    output_dataset = fields.ToOneField("apps.campaign.api.DatasetMetaResource", "output_dataset", blank=True, null=True)
    #tasklet_count = fields.IntegerField(blank=True, null=True)
    status = fields.CharField(blank=True, null=True)
    class Meta:
        resource_name = 'task'
        #authorization = Authorization()
        allowed_methods = ["post", "patch", "put", "get"]
        detail_uri_name = "id"
    
    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object (typically a ``Model`` instance),
        it returns the extra kwargs needed to generate a detail URI.

        By default, it uses the model's ``pk`` in order to create the URI.
        """
        kwargs = {}

        #if isinstance(bundle_or_obj, Bundle):
        #    kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj.obj, self._meta.detail_uri_name)
        #else:
        #    kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj, self._meta.detail_uri_name)

        return kwargs
    
    def get_object_list(self, request):
        return Task.objects.all()._clone()
    
    def obj_get_list(self, bundle):
        return Task.objects.all()._clone()
    
    def dehydrate(self, bundle):
        bundle.data["status"] = bundle.obj.obj.completion()
        return bundle
    
    def obj_get(self, bundle, **kwargs):
        #raise Exception(kwargs)
        bundle.obj = Task.objects.get(id=kwargs["id"])
        return bundle
        
    
    def obj_get_(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get``.

        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.
        """
        try:
            object_list = self.get_object_list(bundle.request).filter(**kwargs)
            stringified_kwargs = ', '.join(["%s=%s" % (k, v) for k, v in kwargs.items()])

            if len(object_list) <= 0:
                raise self._meta.object_class.DoesNotExist("Couldn't find an instance of '%s' which matched '%s'." % (Task, stringified_kwargs))
            elif len(object_list) > 1:
                raise MultipleObjectsReturned("More than '%s' matched '%s'." % (Task, stringified_kwargs))

            bundle.obj = object_list[0]
            self.authorized_read_detail(object_list, bundle)
            return bundle.obj
        except ValueError:
            raise NotFound("Invalid resource lookup data provided (mismatched type).")
    
    def get_obj_detail(self, bundle, **kwargs):
        return bundle
    
        
    def obj_create(self, bundle, **kwargs):
        bundle.obj = Task(procedure_url=bundle.data["ordered_tasks"][0], 
                        input_dataset=bundle.data["input_dataset"], output_dataset=bundle.data["output_dataset"])
        
        bundle.obj.save()
        
        parent_task = bundle.obj
        for t_url in bundle.data["ordered_tasks"][1:]:
            if "aggregator" in t_url:
                continue
            temp_task = Task(procedure_url=t_url, parent=parent_task,
                                input_dataset=bundle.data["output_dataset"], output_dataset=bundle.data["output_dataset"])
            temp_task.save()
            parent_task = temp_task
        
        #now that we've created the dependency chain, we will schedule the first task
        dat = {}
        dat["task"] = bundle.data["ordered_tasks"][0]
        dat["task_id"] = bundle.obj.id
        dat["output_dataset"] = bundle.data["output_dataset"]
        dat["input_dataset"] = bundle.data["input_dataset"]
        dat["cassandra_nodes"] = CassandraNode.get_nodeip_list()
        client = GearmanClient(GearmanNode.get_nodeip_list())
        client.submit_job("pre_schedule", pickle.dumps(dat),background=True)
        
        return bundle.obj
        

