"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import FeedbackForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import FeedbackForm, CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
from .forms import CommentForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ArticleForm




def home(request):
    """Renders the home page."""
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def resources(request):
    return render(request, 'app/resources.html')


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            rating_display = dict(FeedbackForm.RATING_CHOICES).get(int(form.cleaned_data['rating']), form.cleaned_data['rating'])
            
            like_display = []
            for val in form.cleaned_data.get('like_options', []):
                like_display.append(dict(FeedbackForm.LIKE_CHOICES).get(val, val))
            
            visit_display = dict(FeedbackForm.VISIT_CHOICES).get(form.cleaned_data.get('visit_frequency', ''), form.cleaned_data.get('visit_frequency', 'Не указано'))
            
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'rating': rating_display,
                'like_options': like_display,
                'visit_frequency': visit_display,
                'suggestions': form.cleaned_data.get('suggestions', '') or 'Не указано',
            }
            return render(request, 'app/pool.html', {'form': form, 'submitted': True, 'data': data})
        else:
            return render(request, 'app/pool.html', {'form': form, 'submitted': False})
    else:
        form = FeedbackForm()
        return render(request, 'app/pool.html', {'form': form, 'submitted': False})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'app/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')

def blog(request):
    """Страница со списком всех статей блога"""
    articles = Article.objects.all().order_by('-published_date')
    return render(request, 'app/blog.html', {'articles': articles})


def blogpost(request, article_id):
    """Страница отдельной статьи с комментариями"""
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all().order_by('-date') 
    
    form = CommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = article
            comment.save()
            messages.success(request, 'Ваш комментарий добавлен!')
            return redirect('blogpost', article_id=article.id)
    
    context = {
        'article': article,
        'comments': comments,
        'form': form,
    }
    return render(request, 'app/blogpost.html', context)

@staff_member_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            if not article.author:
                article.author = request.user
            article.save()
            return redirect('blog')
    else:
        form = ArticleForm()
    return render(request, 'app/add_article.html', {'form': form})


def video_page(request):
    return render(request, 'app/video.html')