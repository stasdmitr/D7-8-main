from django.views.generic import CreateView
from django.core.mail import send_mail
from .models import Contact
from .forms import ContactForm
from django.shortcuts import render, reverse, redirect
from django.views import View
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "simpleapp/news"



