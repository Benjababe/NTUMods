from django.db import models

# Create your models here.
class TeachingStaff(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    tag = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    profile_pic_url = models.URLField(max_length=200, null=True)
    description = models.TextField()
    appointments = models.ManyToManyField('Appointment')
    interests = models.ManyToManyField('Interest')

    def __str__(self):
        return f"Title: {self.title} Email: {self.email} Tag: {self.tag}"
    
    class Meta:
        verbose_name_plural = 'Teaching Staff'
    
class Appointment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f"{self.name}"
    
class Interest(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f"{self.name}"