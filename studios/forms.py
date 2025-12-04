from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import Application, Category

def validate_cyrillic_name(value):
    if not re.match(r'^[А-ЯЁа-яё\s\-]+$', value):
        raise forms.ValidationError('ФИО должно содержать только кириллические буквы, дефисы и пробелы.')

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(    
        max_length=254,
        required=True,
        validators=[validate_cyrillic_name], 
        label='ФИО',
        help_text='Только кириллические буквы, дефисы и пробелы.'
    )

    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        help_text='Номер телефона в формате +7952', 
        label='Номер телефона',
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Одна большая буква и т.д.',
    )

    email = forms.EmailField(
        required=True,
        help_text='Введите действительный email адрес.',
        label='Email'
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone_number', 'password1', 'password2')

        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
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

