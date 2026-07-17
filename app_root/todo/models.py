from django.db import models

class Task(models.Model):
    task_name = models.CharField(max_length=50)
    is_task_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.task_name[:15]