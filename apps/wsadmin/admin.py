from django.contrib import admin

# Register your models here.

from apps.wsadmin.models import CassandraNode
from apps.wsadmin.models import APINode
from apps.wsadmin.models import WorkerNode
from apps.wsadmin.models import GearmanNode

class BaseAdmin(admin.ModelAdmin):
    list_display = ["ip", "state"]

class CassandraNodeAdmin(BaseAdmin):
    pass

class APINodeAdmin(BaseAdmin):
    pass

class WorkerNodeAdmin(BaseAdmin):
    pass

class GearmanNodeAdmin(BaseAdmin):
    pass

admin.site.register(CassandraNode, CassandraNodeAdmin)
admin.site.register(APINode, APINodeAdmin)
admin.site.register(WorkerNode, WorkerNodeAdmin)
admin.site.register(GearmanNode, GearmanNodeAdmin)


