
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment
from .models import Article



class CustomUserCreationForm(UserCreationForm):
    
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
        required=False
    )
    
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        return username


class CustomAuthenticationForm(AuthenticationForm):
    
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    
    error_messages = {
        'invalid_login': 'Неверное имя пользователя или пароль',
        'inactive': 'Учетная запись не активирована',
    }



class FeedbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
        error_messages={'required': 'Пожалуйста, укажите ваше имя'}
    )
    
    email = forms.EmailField(
        label="Email для связи",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
        error_messages={'required': 'Укажите email', 'invalid': 'Введите корректный email'}
    )
    
    RATING_CHOICES = [
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Удовлетворительно'),
        (2, 'Плохо'),
        (1, 'Ужасно'),
    ]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        label="Оценка сайта",
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        initial=5
    )
    
    LIKE_CHOICES = [
        ('design', 'Дизайн сайта'),
        ('content', 'Содержание и статьи'),
        ('navigation', 'Удобство навигации'),
        ('speed', 'Быстродействие'),
        ('logo', 'Логотип и брендинг'),
    ]
    like_options = forms.MultipleChoiceField(
        choices=LIKE_CHOICES,
        label="Что вам понравилось? (можно выбрать несколько)",
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    VISIT_CHOICES = [
        ('first', 'Первый раз'),
        ('daily', 'Ежедневно'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
        ('rarely', 'Редко'),
    ]
    visit_frequency = forms.ChoiceField(
        choices=VISIT_CHOICES,
        label="Как часто вы посещаете сайт?",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    suggestions = forms.CharField(
        label="Ваши пожелания и комментарии",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 5, 
            'placeholder': 'Напишите, что можно улучшить или добавить...'
        }),
        required=False
    )
    
    consent = forms.BooleanField(
        label="Я согласен на обработку моих персональных данных",
        required=True,
        error_messages={'required': 'Необходимо дать согласие на обработку данных'}
    )
    
class CustomAuthenticationForm(AuthenticationForm):
    
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    
    error_messages = {
        'invalid_login': 'Неверное имя пользователя или пароль',
        'inactive': 'Учетная запись не активирована',
    }

class CommentForm(forms.ModelForm):
    
    text = forms.CharField(
        label="Ваш комментарий",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Напишите ваш комментарий...'
        }),
        required=True,
        error_messages={'required': 'Пожалуйста, введите текст комментария'}
    )
    
    class Meta:
        model = Comment
        fields = ['text']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'short_content', 'full_content', 'image', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'short_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Краткое описание'}),
            'full_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Полный текст статьи'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }