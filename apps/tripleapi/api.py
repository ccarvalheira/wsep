import rdflib
from rdflib import Graph

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL

from rdflib_django.models import NamedGraph
from rdflib_django.models import URIStatement
from rdflib_django.models import LiteralStatement

class GraphResource(ModelResource):
    class Meta:
        queryset = NamedGraph.objects.all()
        resource_name = 'graph'
        authorization = Authorization()



class TripleResource(ModelResource):
    context = fields.ToOneField(GraphResource, "context")
    #subject = fields.CharField("subject")
    class Meta:
        queryset = URIStatement.objects.all()
        resource_name = 'triple'
        authorization = Authorization()
        filtering = {
            "subject": ALL,
            "predicate": ALL,
            "object" : ALL,
            "context": ALL,
        }
        
    
    def obj_get_list(self, bundle, **kwargs):
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        
        sub = rdflib.term.URIRef(filters["subject"]) if "subject" in filters else None
        pred = rdflib.term.URIRef(filters["predicate"]) if "predicate" in filters else None
        ob = rdflib.term.URIRef(filters["object"]) if "object" in filters else None
        con = GraphResource().get_via_uri(filters["context"]) if "context" in filters else None
        
        objs = URIStatement.objects.all()
        if sub:
            objs = objs.filter(subject=sub)
        if pred:
            objs = objs.filter(predicate=pred)
        if ob:
            objs = objs.filter(object=ob)
        if con:
            objs = objs.filter(context=con)
        
        return objs
        
        
    
    
class LiteralStatementResource(ModelResource):
    context = fields.ToOneField(GraphResource, "context")
    class Meta:
        queryset = LiteralStatement.objects.all()
        resource_name = 'literaltriple'
        authorization = Authorization()

   
