from django.db import models
from django.contrib.auth.models import User



class MenuItem(models.Model):
    title = models.CharField("Название" , max_length = 150, blank=False)
    url = models.SlugField(max_length=150, unique=True)
    name = models.CharField("Описание",  max_length = 150, blank=False, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title
