from django.db import models
from django.utils import timezone


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    is_seller = models.BooleanField()
    credits = models.FloatField(max_length=10)

    loc = models.ForeignKey('Location', on_delete=models.CASCADE)

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.email


class Location(models.Model):
    lid = models.AutoField(primary_key=True)
    zip_code = models.IntegerField()
    city_name = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.address

