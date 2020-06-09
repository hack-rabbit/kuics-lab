from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Difficulty)
admin.site.register(Challenge)
admin.site.register(Flag)
admin.site.register(Profile)
admin.site.register(Solve)