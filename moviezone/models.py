from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    ratings = models.DecimalField(max_digits=3, decimal_places=1 )
    netflix_link= models.CharField(max_length= 255)