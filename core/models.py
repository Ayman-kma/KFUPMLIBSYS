from django.db import models
from django.contrib.auth.models import User
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
            "publish_year",
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
        verbose_name=_("books"),
    )
    book_copy_number = models.PositiveIntegerField(
        verbose_name=_("book copy number")
     )
    
    @property
    def is_loaned(self):
        self.book.fetch_related("Book_Loan") ##!!
        return None

class Book_Loan(models.Model):

    books = models.ForeignKey(
        Book, # Check this later
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        verbose_name=_("items"),
    )

    @property
    def total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += (item.quantity * item.price)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = [
            "items",
        ]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        db_index=True,
        verbose_name=_("user"),
    )
    @property
    def full_name(self):
        return self.user.first_name + self.user.last_name
    
    @property
    def username(self):
        return self.user.username


    orders = models.ForeignKey(
    Order,
    on_delete=models.CASCADE,
    blank=True,
    null=False,
    verbose_name=_("orders"),
)

    @property
    def total_payments(self):
        total_payments = 0
        for order in self.orders.all():
            total_payments += order.total_price

        return total_payments

    @property
    def points(self):
        # I will assume that each dollar of payment is equal to the total points
        return self.total_payments

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

        ordering = [
            "orders",
            "user",
        ]

    def __str__(self):
        return self.full_name