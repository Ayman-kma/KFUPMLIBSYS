from django.contrib import admin

from . import models

admin.site.register(models.Book)
admin.site.register(models.Library_People)
admin.site.register(models.Library_Actor)
admin.site.register(models.Subject)
admin.site.register(models.Book_Item)
admin.site.register(models.Book_Loan)
admin.site.register(models.Book_Reserve)
admin.site.register(models.Book_Shelf)
# Register your models here.
