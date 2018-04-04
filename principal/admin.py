from django.contrib import admin
from .models import Service, UserDetails, Curriculum, Feedback

admin.site.register(Service)
admin.site.register(UserDetails)
admin.site.register(Curriculum)
admin.site.register(Feedback)

# Register your models here.