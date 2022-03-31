from django.db import models
from new_app.models import CustomUser
# Create your models here.
class book(models.Model):
    title=models.CharField(max_length=10, blank=True,null=True)
    author=models.CharField(max_length=10,blank=True,null=True)
    relese_date=models.DateField(auto_now=True)
    owner = models.ForeignKey(CustomUser, related_name='books', on_delete=models.CASCADE,default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class BaseModel(models.Model):
    data_created_on=models.DateField(auto_now=True)
    data_updated_on=models.DateTimeField(auto_created=True)
    class Meta:
        abstract=True

class Country(BaseModel):
    country_name=models.CharField(max_length=30)
    short_name=models.CharField(max_length=30)
    status=models.BooleanField(default=True)

