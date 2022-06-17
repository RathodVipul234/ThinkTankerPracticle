from django.contrib import admin
from users.models import User,Hobbies, PersonalDetails
# Register your models here.


admin.site.register(User)
admin.site.register(Hobbies)
admin.site.register(PersonalDetails)