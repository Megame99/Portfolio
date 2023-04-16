
# Create your models here.

from django.db import models







class Quest(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(blank=True)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=250)
    location = models.CharField(max_length=200)
    id = models.PositiveIntegerField(unique=True, primary_key=True, auto_created =True)
    class Meta:
        db_table = "quests"
        

