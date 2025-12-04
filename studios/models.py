from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    full_name = models.CharField(max_length=256, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return f"{self.full_name}"
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_plan = models.ImageField(upload_to='application_plans/', max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    image_design = models.ImageField(upload_to='application_designs/', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('application_detail', kwargs={'pk': self.pk})