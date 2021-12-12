from django.contrib import admin

from .models import Dog, Profile


# admin.site.unregister((Dog))
admin.site.register((Dog))

admin.site.register((Profile))

# Register your models here.
