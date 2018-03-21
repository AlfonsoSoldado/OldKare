from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    avaliability = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.date}'

    def short_description(self):
        return self.description[:15]

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField()
    phone = models.CharField(max_length=100)
    postalAddress = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    socialReferences = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}'