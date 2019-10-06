from datetime import datetime

from django.db import models


# class BaseModel(Model):
#     @classmethod
#     def db(cls):
#         return MongoClient()['my_database_name']
#
#
# class Bin(Document):
#     current_filled       = IntField(min_value=0)
    # next_collection_time = DateTimeField()
    # current_time         = DateTimeField()
    # is_full              = BooleanField()
    # has_leak             = BooleanField()

    # def __str__(self):
    #     return self.id

# class Bin(models.Model):
#     current_filled = models.IntegerField(null=False)
#     next_collection_time = models.DateTimeField(default=datetime.now(), )
#     current_time = models.DateTimeField(default=datetime.now(), blank=True, null=True)
#     is_full      = models.BooleanField(default=False, blank=True, null=False)
#     has_leak     = models.BooleanField(default=False, blank=True, null=False)
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#
#         if self.current_filled == 100:
#             self.is_full = True
#
#         if self.current_temp > 50:
#             self.has_overheat = True
#
#         # self.save()
#
#     def __str__(self):
#         return str(self.id)


# class Facility(models.Model):
#     name = models.CharField(max_length=64)
#     address = models.CharField(max_length=64)
#     bins = models.ManyToManyField(Bin, related_name='facility')
#     map_path = models.CharField(max_length=512)
#
#     def __str__(self):
#         return self.name
