from django.contrib import admin
from .models import User, Client, Sale, Payment
# Register your models here.

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Sale)
admin.site.register(Payment)