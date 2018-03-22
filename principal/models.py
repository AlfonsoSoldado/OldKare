from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Service(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    avaliability = models.IntegerField()
    offerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offerer", null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.date}'

    def short_description(self):
        return self.description[:15]

    def get_absolute_url(self):
        return u'/oldkareall'

class UserDetails(models.Model):
    GENDER_CHOICES = (
        ('M', 'Mujer'),
        ('H', 'Hombre'),
        ('O', 'Otro'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número debe seguir el siguiente patrón: '+999999999'. Máximo 15 dígitos.")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField()
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    postalAddress = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=100)
    photo = models.CharField(max_length=600)
    socialReferences = models.CharField(null=True,blank=True,max_length=600)

    def __str__(self):
        return f'{self.user.username}'
    def get_absolute_url(self):
        return u'/oldkare'