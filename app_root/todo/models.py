from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_task_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.task_name[:15]
