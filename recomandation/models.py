from django.db import models

# Create your models here.
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.CharField(max_length=500)
    password=models.CharField(max_length=30)
    

class User(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    phone=models.CharField(max_length=30,unique=True)
    address=models.CharField(max_length=500)
    email=models.CharField(max_length=500,unique=True)
    password=models.CharField(max_length=30)

class Commonnutrition(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    category=models.CharField(max_length=500)
    description=models.CharField(max_length=500)
    date=models.CharField(max_length=500)
    image = models.ImageField(upload_to='Images/')


class Disease(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    subtype=models.CharField(max_length=500)
    
class Nutritionrequirements(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    nutrient_type=models.CharField(max_length=500)
    s_range=models.CharField(max_length=100)
    e_range=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    date=models.CharField(max_length=100)
    disease=models.ForeignKey(Disease,on_delete=models.CASCADE)



class Testlabvalues(models.Model):
    id=models.AutoField(primary_key=True)
    lab_value=models.CharField(max_length=500)
    
    date=models.CharField(max_length=100)

    diseases=models.ForeignKey(Disease,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Feedback(models.Model):
    id=models.AutoField(primary_key=True)
    feedback=models.CharField(max_length=500)
    date=models.CharField(max_length=100)
    users=models.ForeignKey(User,on_delete=models.CASCADE)
    