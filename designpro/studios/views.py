from django.shortcuts import render

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
