from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Application, Category
from .forms import ApplicationForm
from .models import Profile
from django.views import generic
from django.urls import reverse_lazy

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

