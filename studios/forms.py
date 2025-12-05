from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Category
from studios.models import Profile
from django import forms
import re

def validate_cyrillic_name(value):
    if not re.match(r'^[А-ЯЁа-яё\s\-]+$', value):
        raise forms.ValidationError('ФИО должно содержать только кириллические буквы, дефисы и пробелы.')
    
def validate_username(value):
    if not re.match(r'^[a-zA-Z\-]+$', value):
        raise forms.ValidationError('Логин должен содержать только латинские буквы и дефисы.')


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(    
        max_length=254,
        required=True,
        validators=[validate_cyrillic_name], 
        label='ФИО',
        help_text='Только кириллические буквы, дефисы и пробелы.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'})
    )

    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        help_text='Номер телефона в формате +7952', 
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXX'})
    )

    email = forms.EmailField(
        required=True,
        help_text='Введите действительный email адрес.',
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'})
    )
    consent = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        help_text='Вы должны согласиться с обработкой персональных данных.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Введите надежный пароль.',
    )

    username = forms.CharField(
        validators=[validate_username], # Применяем валидатор
        help_text='Только латинские буквы и дефисы.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'myusername'})
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') # full_name и consent добавим вручную в save

    

        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.full_name = self.cleaned_data["full_name"]
            profile.phone_number = self.cleaned_data["phone_number"]
            profile.consent = self.cleaned_data["consent"] 
            if commit:
                profile.save()
        return user


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image_plan']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название заявки'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image_plan': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'image_plan': 'Фото/План помещения (jpg, jpeg, png, bmp, макс. 2Мб)',
        }

    def clean_image_plan(self):
        image = self.cleaned_data.get('image_plan')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла превышает 2 МБ.')
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
                raise forms.ValidationError('Неподдерживаемый формат файла. Разрешены: jpg, jpeg, png, bmp.')
        return image



# ------------ Admin ------------

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название категории'}),
        }
        labels = {
            'name': 'Название категории',
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('Категория с таким названием уже существует.')
        return name

