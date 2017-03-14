from django.contrib import admin
from .models import *

admin.site.register(MyTestimony)
admin.site.register(Testimonies)
admin.site.register(SharedTestimonies)
admin.site.register(Tag)
admin.site.register(UserFollowers)

# Register your models here.
