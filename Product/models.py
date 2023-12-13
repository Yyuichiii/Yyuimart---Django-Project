from django.db import models


class all_Products(models.Model):       # COMM0N TO ALL PRODUCTS
    Brand=models.CharField(max_length=15,null=True)
    PName=models.CharField(max_length=20,null=True,verbose_name='Product Name')
    Description=models.TextField(null=True)
    Price=models.PositiveBigIntegerField(null=True)
    Quantity=models.IntegerField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.Brand} {self.PName}"
  


class Mobile(all_Products):
    def format():
        n = Mobile.objects.count()
        return 'M'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    PImage=models.ImageField(upload_to='Mobile',null=True,verbose_name='Product Image')
    
    class Meta:
        ordering = ("PID",)

class Laptop(all_Products):
    def format():
        n = Laptop.objects.count()
        return 'L'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    PImage=models.ImageField(upload_to='Laptop',null=True,verbose_name='Product Image')
    
    class Meta:
        ordering = ("PID",)

class HeadPhone(all_Products):
    def format():
        n = HeadPhone.objects.count()
        return 'H'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    PImage=models.ImageField(upload_to='HeadPhone',null=True,verbose_name='Product Image')
    
    class Meta:
        ordering = ("PID",)


class Men(all_Products):
    def format():
        n = Men.objects.count()
        return 'MF'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    PImage=models.ImageField(upload_to='Men',null=True,verbose_name='Product Image')
    
    class Meta:
        ordering = ("PID",)

class Women(all_Products):
    def format():
        n = Women.objects.count()
        return 'W'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    PImage=models.ImageField(upload_to='Women',null=True,verbose_name='Product Image')
    class Meta:
        ordering = ("PID",)

class Shoe(all_Products):
    def format():
        n = Shoe.objects.count()
        return 'S'+str(n+1)
    PID=models.CharField(max_length=10,primary_key=True,unique=True,default=format)
    PImage=models.ImageField(upload_to='Shoe',null=True,verbose_name='Product Image')
    
    class Meta:
        ordering = ("PID",)

   
    
