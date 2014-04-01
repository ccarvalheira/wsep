from django.contrib import admin

# Register your models here.

from apps.wsusers.models import WSUser
from apps.wsusers.models import Permission


class WSUserAdmin(admin.ModelAdmin):
	pass
	
class PermissionAdmin(admin.ModelAdmin):	
    pass
    
    
admin.site.register(WSUser, WSUserAdmin)
admin.site.register(Permission, PermissionAdmin)
