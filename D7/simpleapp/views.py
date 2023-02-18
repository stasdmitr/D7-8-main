import os
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News, Articles, Author
from .filters import NewsFilter, ArticlesFilters
from .forms import NewsForm, ArticlesForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.core.mail import send_mail
from .models import Appointment
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = News
    ordering = 'name'
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = News
    # Используем другой шаблон — product.html
    template_name = 'concrete_News.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'


# Добавляем новое представление для создания товаров.
class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = NewsForm
    permission_required = ("simpleapp.add_news")
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = News
    template_name = 'news_edit.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get_or_create(user=user)[0]
            post.save()
            return self.form_valid(form)
        return redirect('news')


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    permission_required = ("simpleapp.add_news")
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = News
    template_name = 'news_edit.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get_or_create(user=user)[0]
            post.save()
            return self.form_valid(form)
        return redirect('news')


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ("simpleapp.delete_news")
    template_name = 'news_delete.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('news')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)


class NewsSearch(ListView):
    model = News
    template_name = 'news_search.html'
    # Указываем модель, объекты которой мы будем выводить
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# ______________________________________________________________________________________


class ArticlesList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Articles
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'articles.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = ArticlesFilters(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ArticlesDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Articles
    # Используем другой шаблон — product.html
    template_name = 'concrete_Articles.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'articles'


# Добавляем новое представление для создания товаров.
class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ("simpleapp.add_articles")
    form_class = ArticlesForm
    model = Articles
    template_name = 'articles_edit.html'
    context_object_name = 'articles_create'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get_or_create(user=user)[0]
            post.save()
            return self.form_valid(form)
        return redirect('articles')


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ("simpleapp.add_articles")
    form_class = ArticlesForm
    model = Articles
    template_name = 'articles_edit.html'
    context_object_name = 'articles_create'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get_or_create(user=user)[0]
            post.save()
            return self.form_valid(form)
        return redirect('articles')


class ArticlesDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ("simpleapp.delete_articles")
    template_name = 'articles_delete.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('articles')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Articles.objects.get(pk=id)


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'], )
        appointment.save()
        html_content = render_to_string(
            'appointment_created.html',
            {'appointment': appointment, })
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='dmitrive2010@yandex.ru',
            to=['dnitrive2010@gmail.com'], )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('make_appointment')