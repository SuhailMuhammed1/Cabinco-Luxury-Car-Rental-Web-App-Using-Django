from django.db import models

# Create your models here.
class admin_login_tb (models.Model):
	name=models.CharField( max_length=100, default='')
	email=models.CharField( max_length=100, default='')
	password=models.CharField(max_length=300, default='')

class car_tb (models.Model):
	image=models.FileField(upload_to='cars')
	name=models.CharField( max_length=300, default='')
	people=models.CharField(max_length=300, default='')
	fuel=models.CharField(max_length=300, default='')
	miles=models.CharField(max_length=300, default='')
	transmission=models.CharField(max_length=300, default='')

