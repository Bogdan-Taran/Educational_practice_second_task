from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Application, Category
from .forms import ApplicationForm, CategoryForm
from .models import Profile
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
import os

def index(request):
    return render(
        request,
        'index.html',
    )

def home(request):
    return render(
        request,
        'base_generic.html'
    )
def neworder(request):
    return render(
        request,
        'new_order.html'
    )


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            Profile.objects.create(user=user, phone_number=form.cleaned_data.get('phone_number'))
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
        success_url = reverse_lazy('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user 
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('my_applications') 
    else:
        form = ApplicationForm()

    return render(request, 'studios/application_form.html', {'form': form})

@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    paginator = Paginator(applications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'studios/my_applications.html', {'page_obj': page_obj})

@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user) 

    if application.status != 'new':
        messages.error(request, f'Невозможно удалить заявку "{application.title}" с текущим статусом "{application.get_status_display()}".')
        return redirect('my_applications')

    if request.method == 'POST':
        application.delete()
        messages.success(request, f'Заявка "{application.title}" успешно удалена.')
        return redirect('my_applications')

    return render(request, 'studios/application_confirm_delete.html', {'application': application})





# ------------- Admin --------------

@staff_member_required
def admin_applications(request):
    # список всех заявок для админа
    applications = Application.objects.select_related('user', 'category').order_by('-created_at')

    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')

    if status_filter:
        applications = applications.filter(status=status_filter)
    if category_filter:
        applications = applications.filter(category__id=category_filter)


    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    categories = Category.objects.all()

    return render(request, 'studios/admin_applications.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_status': status_filter,
        'selected_category': category_filter,
    })

@staff_member_required
def change_application_status(request, pk):
    # изменить статус заявки админом
    application = get_object_or_404(Application, pk=pk)


    if application.status in ['in_progress', 'completed']:
        messages.error(request, f'Невозможно изменить статус заявки "{application.title}", так как она уже "{application.get_status_display()}".')
        return redirect('admin_applications')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        comment = request.POST.get('comment', '').strip()
        image_design = request.FILES.get('image_design')

        
        if new_status not in ['in_progress', 'completed']:
            messages.error(request, 'Некорректный статус.')
            return redirect('change_application_status', pk=pk)

        
        if new_status == 'in_progress' and not comment:
            messages.error(request, 'Для статуса "Принято в работу" необходимо указать комментарий.')
            return redirect('change_application_status', pk=pk)

        if new_status == 'completed' and not image_design:
            messages.error(request, 'Для статуса "Выполнено" необходимо прикрепить изображение дизайна.')
            return redirect('change_application_status', pk=pk)

        
        if image_design:
            if image_design.size > 2 * 1024 * 1024:
                messages.error(request, 'Размер файла изображения превышает 2 МБ.')
                return redirect('change_application_status', pk=pk)
    
            ext = os.path.splitext(image_design.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
                messages.error(request, 'Неподдерживаемый формат файла изображения. Разрешены: jpg, jpeg, png, bmp.')
                return redirect('change_application_status', pk=pk)

        
        try:
            with transaction.atomic():
                application.status = new_status
                application.comment = comment
                if image_design:
                    application.image_design = image_design
                application.save()
            messages.success(request, f'Статус заявки "{application.title}" успешно изменён на "{application.get_status_display()}".')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при сохранении: {str(e)}')

        return redirect('admin_applications')

   
    return render(request, 'studios/change_status.html', {'application': application})

@staff_member_required
def manage_categories(request):
    # отобразтьб список категорий и форму для добавления новой
    categories = Category.objects.all()
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена.')
            return redirect('manage_categories')
        else:
            categories = Category.objects.all()

    return render(request, 'studios/manage_categories.html', {'categories': categories, 'form': form})

@staff_member_required
def add_category(request):
    # представление для добавления категории
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена.')
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'studios/add_category.html', {'form': form})

@staff_member_required
def delete_category(request, pk):
    # удалть категорию и все заявки связанные с ней
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category_name = category.name
        category.delete() # каскадное удаление
        messages.success(request, f'Категория "{category_name}" и все связанные заявки успешно удалены.')
        return redirect('manage_categories')

    return render(request, 'studios/category_confirm_delete.html', {'category': category})