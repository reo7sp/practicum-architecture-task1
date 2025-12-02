from django.db import models


class Device(models.Model):
    manufacturer_id = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'
        unique_together = [['manufacturer_id', 'device_id']]
