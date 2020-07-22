from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from . forms import *

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


def ContactUs(request):

    form = ContactUsForm()
    print("Hello")
    if request.method == 'POST':
        print("POST")
        
        form = ContactUsForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            message1 = request.POST.get('message')
            
            message2 = request.POST.get('name')
            message3 = request.POST.get('email')
            
            message =  'Message : ' + message1 + '\n' + 'Name : ' + message2 + '\n' +  'Email : \t' + message3
            

            send_mail('Contact us Form Filled by the User',
            message,
            settings.EMAIL_HOST_USER,
            ['nikhil.k18@iiits.in'],
            fail_silently=False)

            return home(request)

        else:
            #form = ContactUsForm()
            print("Error Form!")

    else:
        #form = ContactUsForm()
        print ("This must be GET")
    return render(request,'blog/contact.html',{'form':form})
