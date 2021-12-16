from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Library_Actor(models.Model):
    Actor_Type = models.integer_field(
        unique=True,
        primary_key=True,
        null=False,
        blank=False
    )


class Library_People(models.Model):
    # People_ID????
    People_ID = models.integer_field(
        unique=True,
        primary_key=True,
        max_length=8,
        null=False,
        blank=False,
        # verbose_name=_("")
    )
    First_Name = models.CharField(
        max_length=256,
        blank=False,
        null=False
    )
    Last_Name = models.CharField(
        max_length=256,
        blank=False,
        null=False
    )
    People_Type = models.ForeignKey(
        Library_Actor,
        on_delete=models.CASCADE,
        blank=False,
        null=False,)

    Birth_Date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("publish date")
    )
    SEX_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female',),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        null=False,
        blank=False,
    )

    Department = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    Contact_Number = models.phonenumber_field(blank=True, null=True)

    Email = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
