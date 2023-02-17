from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)




class News(models.Model):
    date = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(default = "News post")
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',  # все продукты в категории будут доступны через поле products
    )
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'



class Articles(models.Model):
    date = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="Articles_post")

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='articles',  # все продукты в категории будут доступны через поле products
    )

    def get_absolute_url(self):
        return reverse('articles_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name.title()


