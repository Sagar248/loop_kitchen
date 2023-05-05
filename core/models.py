from django.db import models

# Create your models here.

# class Report(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='post_images')
#     caption = models.TextField()
#     created_at = models.DateTimeField(default=datetime.now)
#     no_of_likes = models.IntegerField(default=0)


class OpenHours(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.CharField(max_length=25)
    day = models.IntegerField()
    timezone_str = models.CharField(max_length=100, null=True)
    local_open_time = models.TimeField()
    local_close_time = models.TimeField()
    utc_open_time = models.TimeField(null=True)
    utc_close_time = models.TimeField(null=True)


class OpenHoursUTC(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.CharField(max_length=25)
    day = models.IntegerField()
    timezone_str = models.CharField(max_length=100, null=True)
    utc_open_time = models.TimeField()
    utc_close_time = models.TimeField()

class StoreStatus(models.Model):
    id = id = models.IntegerField(primary_key=True)
    store_id = models.CharField(max_length=25)
    status = models.CharField(max_length=25)
    timestamp_utc = models.DateTimeField()

class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.CharField(max_length=25)
    uptime_last_hour = models.IntegerField()
    uptime_last_day = models.IntegerField()
    uptime_last_week = models.IntegerField()
    downtime_last_hour = models.IntegerField()
    downtime_last_day = models.IntegerField()
    downtime_last_week = models.IntegerField()
    


