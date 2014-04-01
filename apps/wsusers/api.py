from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.bundle import Bundle

from django.core.urlresolvers import resolve, get_script_prefix

from django.contrib.auth.hashers import make_password

from apps.wsusers.models import WSUser
from apps.wsusers.models import Permission

from apps import *

class WSUserResource(ModelResource):
    class Meta:
        queryset = WSUser.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        fields = ["name", "affiliation",  "username", "password"]
        allowed_methods = ["get", "post", "patch", "delete"]
        
    
    def dehydrate_password(self, bundle):
        return ""
        
    def hydrate_password(self, bundle):
        bundle.data["password"] = make_password(bundle.data["password"])
        return bundle

class PermissionResource(ModelResource):
    class Meta:
        queryset = Permission.objects.all()
        resource_name = "permission"
        authorization = Authorization()
        #excludes = ["object_type", "object_id"]
    
    def get_pk_from_uri(self, uri):
        prefix = get_script_prefix()
        chomped_uri = uri

        if prefix and chomped_uri.startswith(prefix):
            chomped_uri = chomped_uri[len(prefix)-1:]

        try:
            view, args, kwargs = resolve(chomped_uri)
        except Resolver404:
            raise NotFound("The URL provided '%s' was not a link to a valid resource." % uri)

        return kwargs["pk"], kwargs["resource_name"]
    
    def hydrate_object_type(self, bundle):
        
        pk, name = self.get_pk_from_uri(bundle.data["object_url"])
        
        bundle.data["object_type"] = name.title()
        return bundle
        
    def hydrate_object_id(self, bundle):
    
        pk, name = self.get_pk_from_uri(bundle.data["object_url"])
        bundle.data["object_id"] = pk
        
        return bundle
    
    def dehydrate_object_type(self, bundle):
        return ""
    
    def dehydrate_object_id(self, bundle):
        return ""
