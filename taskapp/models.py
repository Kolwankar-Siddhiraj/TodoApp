from django.db import models

# Create your models here.


class Task(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    due_date = models.DateField(blank=True, null=True)
    # status => in-progress | complete | incomplete
    status = models.CharField(max_length=32, default="in-progress")

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

