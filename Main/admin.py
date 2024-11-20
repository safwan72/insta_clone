from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Posts)
admin.site.register(models.Image)
admin.site.register(models.Hashtag)
admin.site.register(models.Comment)
admin.site.register(models.Story)
admin.site.register(models.Like)