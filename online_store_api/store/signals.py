from django.db.models.signals import post_save
from django.dispatch import receiver 
from .models import Order, Product 
from django.core.mail import send_mail 

