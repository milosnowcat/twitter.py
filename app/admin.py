from django.contrib import admin
from .models import Profile, Relationship, Ban, Client

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Ban)
admin.site.register(Client)
