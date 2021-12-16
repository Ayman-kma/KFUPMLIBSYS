from django.contrib import admin

from . import models

admin.site.register(models.Book)
admin.site.register(models.Author)
admin.site.register(models.Member)
admin.site.register(models.System)
admin.site.register(models.Librarian)
admin.site.register(models.Subject)
admin.site.register(models.Book_Item)
admin.site.register(models.Book_Loan)
admin.site.register(models.Book_Reserve)
admin.site.register(models.Book_Shelf)
# Register your models here.
