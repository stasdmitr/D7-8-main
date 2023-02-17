from django.views.generic import CreateView
from django.core.mail import send_mail
from .models import Contact
from .forms import ContactForm
from django.shortcuts import render, reverse, redirect
from django.views import View


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "simpleapp/news"

