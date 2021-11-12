from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# Create your models here.



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)



    # owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    # highlighted = models.TextField()
