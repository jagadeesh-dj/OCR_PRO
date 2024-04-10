# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Files(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='User')
    file=models.FileField(upload_to='my_file')
    timestamp=models.DateTimeField(auto_now_add=True)


class TxtFiles(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.IntegerField()
    name=models.CharField(max_length=30,unique=True)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
