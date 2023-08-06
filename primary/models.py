from django.db import models
from django.contrib.auth.models import User

# SuperUser

# username: beacon
# password: BCEN23


# Users
# username : Callahan
# password : 1234567*

# username : Evan Mendonsa
# password : 123

# username : Melvin
# password : melviniscool

# username : Reeve
# password : lock1234

# username : Jackson Simons
# password : jks

# username : John
# password : john

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    college = models.CharField(max_length=200)
    phone = models.IntegerField()
    isAdmin = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.user)
    

class Post(models.Model):
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=200)
    description = models.TextField()
    college = models.CharField(max_length=200)
    sdate = models.DateTimeField()
    edate = models.DateTimeField()
    post_images = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.title

