from django.contrib import admin
from .models import User, Hobbi, Message, Hobbies
# Register your models here.
admin.site.register(Message)
admin.site.register(User)
admin.site.register(Hobbi)
admin.site.register(Hobbies)