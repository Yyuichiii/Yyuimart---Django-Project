from django.db import models


class Mobile(models.Model):
    def format():
        n = Mobile.objects.count()
        return 'M'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    Brand=models.CharField(max_length=10,blank=False)
    PName=models.CharField(max_length=12,blank=False)
    PImage=models.ImageField(upload_to='Mobile',blank=False)
    Description=models.TextField(blank=False)
    Price=models.PositiveBigIntegerField(blank=False)
    Quantity=models.IntegerField(default=0)

    class Meta:
        ordering = ("PID",)

    def __str__(self):
        return f"{self.Brand} {self.PName}"
    
