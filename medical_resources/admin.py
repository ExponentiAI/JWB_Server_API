from django.contrib import admin

# Register your models here.
# Register your models here.
from medical_resources.models import *

# admin.site.register()
from medical_resources.models import Demand, UserInfo, Material

admin.site.register([Demand, UserInfo, Material])
