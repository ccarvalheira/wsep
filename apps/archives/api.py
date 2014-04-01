from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from tastypie import fields

from apps.archives.models import Archive

from apps.campaign.api import DatasetMetaResource
from apps.campaign.api import CampaignResource

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            #raise Exception(request.FILES)
            data = request.POST.copy()
            data.update(request.FILES)

            return data

        return super(MultipartResource, self).deserialize(request, data, format)

class ArchiveResource(MultipartResource, ModelResource):
    dataset = fields.ForeignKey(DatasetMetaResource, "datasetmeta", blank=True, null=True)
    campaign = fields.ForeignKey(CampaignResource, "campaign", blank=True, null=True)
    
    file_field = fields.FileField(attribute="file_field")

    class Meta:
        queryset = Archive.objects.all()
        resource_name = 'archive'
        authorization = Authorization()
        
        fields = ["file_field", "name"]


