from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Subject(models.Model):
    subject_name= models.CharField(
        max_length= 512,
        blank= False,
        null = False
    )
    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")
        ordering = [
            "subject_name",
        ]

    

def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Book(models.Model):
    ISBN_code = models.CharField(
        unique=True,
        primary_key=True,
        max_length=64,
        null = False,
        blank= False,
        verbose_name= _("ISBN code")
    )

    book_title = models.CharField(
    max_length=512,
    blank=False,
    null=False,
    verbose_name=_("book title"),
    )

    book_language = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("book language")
    )

    no_of_copies = models.PositiveIntegerField(
        null = True, 
        blank= True,
        verbose_name= _("number of copies")
    )

    subject = models.ForeignKey(
        Subject,
        on_delete= models.CASCADE,
        null= True,
        blank= True,
        verbose_name=_("subject")
    )

    @property
    def is_available(self):
        return self.no_of_copies > 0
    
    authors = models.ManyToManyField(
    Library_People,
    on_delete= models.CASCADE,
    max_length=32,
    blank=True,
    null=False,
    verbose_name=_("authors"),
    ) ## RECHECK THIS


    publication_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1800), max_value_current_year],
        blank= True,
        null = True,
        verbose_name= _("publication year")
    )


    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")

        ordering = [
            "publication_year",
            "book_title",
        ]

    def __str__(self):
        return self.book_title

class Book_Item(models.Model):
    bar_code = models.CharField(
        max_length=32,
        unique=True,
        primary_key=True,
        verbose_name= _("bar code")
    )
    book = models.ForeignKey(
        Book, # Check this later
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        verbose_name=_("book"),
    )
    book_copy_number = models.PositiveIntegerField(
        verbose_name=_("book copy number")
     )
    loan_status = models.BooleanField(
        verbose_name=_("loan status")
    )

    class Meta:
        verbose_name = _("book item")
        verbose_name_plural = _("book items")

        ordering = [
            "bar_code",
            "book",
        ]

    def __str__(self):
        return self.bar_code

class Book_Loan(models.Model):
    borrower = models.ForeignKey(
        Library_People,
        on_delete= models.CASCADE,
        verbose_name= _("issued by")
    )

    book_item = models.ForeignKey(
        Book_Item,
        on_delete= models.CASCADE,
        verbose_name= _("book item")
    )

    borrowed_from = models.DateField(
        verbose_name=_("borrowed from"),
        null = False,
    )
    borrowed_to = models.DateField(
        verbose_name=_("borrowed to"),
        null = False,
    )

    actual_return = models.DateField(
        verbose_name=_("borrowed to"),
        null = True,
        blank = True,
    )

    issued_by = models.ForeignKey(
        Library_People,
        on_delete= models.CASCADE,
        verbose_name= _("issued by")
    )

    class Meta:
        constraints = [
            # This constraint assuers that the borrower, bar_code,
            # and borrowed from are unique in the table.
            models.UniqueConstraint(
                fields= ["borrower", "book_item", "borrowed_from"],
                name= "unique composite primary key",
                ),
        ]
        verbose_name = _("book loan")
        verbose_name_plural = _("book loans")
        ordering = [
            "borrowed_from",
        ]


class Book_Reserve(models.Model):
    borrower = models.ForeignKey(
        Library_People,
        on_delete= models.CASCADE,
        verbose_name= _("borrower")
    )

    book = models.ForeignKey(
        Book, # Check this later
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        verbose_name=_("book"),
    )

    reserve_date = models.DateField(
        verbose_name=_("reserve date"),
    )

    reserve_status = models.BooleanField(
        verbose_name=_("reserve status")
    )

    class Meta:
        constraints = [
            # This constraint assuers that the borrower, bar_code,
            # and borrowed from are unique in the table.
            models.UniqueConstraint(
                fields= ["borrower", "book"],
                name= "unique composite primary key",
                ),
        ]
        verbose_name = _("book reserve")
        verbose_name_plural = _("book reserves")
        ordering = [
            "reserve_date",
        ]