from django.db import models


class Base(models.Model):
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Name(Base):
    title = models.CharField(max_length=20)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)


class Picture(Base):
    large = models.URLField()
    medium = models.URLField()
    thumbnail = models.URLField()


class Timezone(Base):
    offset = models.CharField(max_length=20)
    description = models.TextField(blank=True, default='')


class Coordinates(Base):
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)


class Location(Base):
    region = models.CharField(max_length=15)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    postcode = models.IntegerField()
    coordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)
