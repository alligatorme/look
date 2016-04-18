from django.db import models

# Create your models here.

class brief(models.Model):	
	imay=models.CharField(max_length=15,primary_key=True)
	info=models.CharField(max_length=200)
	sha1=models.CharField(max_length=40,default='')
	swap=models.CharField(max_length=40,default='')
	comd=models.CharField(max_length=40,default='')


class detail(models.Model):
	head=models.ForeignKey(brief)
	node=models.CharField(max_length=40)
	lump=models.CharField(max_length=300)
