from django.shortcuts import render


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return render(request, 'blog/home.html')
        else:
            return render(request, 'blog/store_home.html')
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/aboutus.html')


def menu(request):
    return render(request, 'blog/menu.html')


def contact(request):
    return render(request, 'blog/contact.html')
