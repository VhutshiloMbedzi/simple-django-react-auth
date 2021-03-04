from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

def upload_profile_picture(instance, filename):
    return "profile/{user}/{filename}".format(user=instance.user, filename=filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False, null=True)
    bio = models.TextField(max_length=265, blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(upload_to=upload_profile_picture, blank=True, null=False)

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.user