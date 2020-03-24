from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_store_owner = models.BooleanField(default=False)
    #
    # class Meta(AbstractUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserFeedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    Feedback = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
