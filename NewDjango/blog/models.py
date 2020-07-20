from django.db import models

class ContactUs(models.Model):
    
    
    message = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()


    def __str__(self):
        return self.name

