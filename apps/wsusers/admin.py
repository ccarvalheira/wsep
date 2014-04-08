from django.contrib import admin

# Register your models here.

from apps.wsusers.models import WSUser
from apps.wsusers.models import CPermission


class WSUserAdmin(admin.ModelAdmin):
	pass
	
class CPermissionAdmin(admin.ModelAdmin):	
    pass
    
    
admin.site.register(WSUser, WSUserAdmin)
admin.site.register(CPermission, CPermissionAdmin)
