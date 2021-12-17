from django import template
import os, sys
from core.models import Librarian, Member


register = template.Library() 

@register.filter(name='belongs_to_librarian') 
def belongs_to_librarian(user):
    return Librarian.objects.filter(user=user).exists()

@register.filter(name='belongs_to_member') 
def belongs_to_member(user):
    return Member.objects.filter(user=user).exists()