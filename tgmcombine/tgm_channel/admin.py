from django.contrib import admin

# Register your models here.
from .models import TgmChannel, CatName, CategoriesMatch

admin.site.register(TgmChannel)
admin.site.register(CatName)
admin.site.register(CategoriesMatch)

