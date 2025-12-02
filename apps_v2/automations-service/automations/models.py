from django.db import models
import uuid
import json


class Scenario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    name = models.CharField(max_length=255)
    scenario = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scenarios'
        indexes = [
            models.Index(fields=['user_id']),
        ]
