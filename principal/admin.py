from django.contrib import admin
from .models import Service, UserDetails, Curriculum

admin.site.register(Service)
admin.site.register(UserDetails)
admin.site.register(Curriculum)

# Register your models here.