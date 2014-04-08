from django.db import models
from django.core.exceptions import ValidationError

from apps.dataviewer.models import Aggregator
from apps.dataviewer.models import Filter
from apps.dataviewer.models import Calculator

class Task(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    procedure_url = models.TextField()
    input_dataset = models.TextField()
    output_dataset = models.TextField()
    tasklet_count = models.IntegerField(default=0)
    done = models.BooleanField(default = False)
    
    def __unicode__(self):
        return self.procedure_url + " - " + (self.parent.procedure_url if self.parent else "root task")
    
    
    def completion(self):
        all_tasks = self.task_set.all()
        
        if self.done:
            if all_tasks:
               return all_tasks.all()[0].completion()
            else:
               return 0
        else:
            if self.tasklet_count == 0:
                if all_tasks:
                    return all_tasks.all()[0].completion()+10
                else:
                    return 10
            else:
                return self.tasklet_count
        return 0
        
