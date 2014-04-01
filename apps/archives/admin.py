from django.contrib import admin

from apps.archives.models import Archive
#from apps.archives.models import ArchiveType
#from apps.archives.models import CampaignDoc




class ArchiveAdmin(admin.ModelAdmin):
    pass

admin.site.register(Archive, ArchiveAdmin)



