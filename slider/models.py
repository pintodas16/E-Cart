from django.db import models

# Create your models here.


class Slider(models.Model):
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'photos/slider')
    
    class Meta:
        verbose_name = 'slider'
        verbose_name_plural = 'slideres'
    
    def __str__(self):
        return self.title

