from django.contrib import admin

from .models import Dog, Profile, Comment, Post


# admin.site.unregister((Dog))
admin.site.register((Dog))

admin.site.register((Profile))
admin.site.register((Comment))
admin.site.register((Post))

# Register your models here.
