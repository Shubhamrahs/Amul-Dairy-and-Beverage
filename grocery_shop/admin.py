from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Owner)
admin.site.register(Employee)
admin.site.register(Inventory)
admin.site.register(Cart)