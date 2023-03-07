from django.db import models
from api.models import Readings

# Create your models here.
class EVChargingLocation(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    level = models.IntegerField()
    def __str__(self):
        return self.station_name

class Tracker(models.Model):
    tracker_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.tracker_name