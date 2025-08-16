from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from typing import List
from pydantic import BaseModel, Field




class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    ssteps = models.JSONField(default=list, blank=True, null=True)
    steps = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.todo_name
    

class Ai_todo_steps(BaseModel):
    steps : List[str] = Field([], description="the steps which needed to be taken to do the task")