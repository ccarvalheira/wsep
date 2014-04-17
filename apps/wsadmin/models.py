from django.db import models

# Create your models here.


class Node(models.Model):
    ip = models.CharField(max_length=15)
    state = models.BooleanField()
    
    class Meta:
        abstract = True

class CassandraNode(Node):
    
    @classmethod
    def get_nodeip_list(self):
        node_list = [c.ip for c in self.objects.all()[:5]]
        return ["127.0.0.1"]

class APINode(Node):
    pass

class WorkerNode(Node):
    pass

class GearmanNode(Node):
    
    @classmethod
    def get_nodeip_list(self):
        node_list = [g.ip for g in self.objects.filter(state=True)[:5]]
        return ["127.0.0.1"]


