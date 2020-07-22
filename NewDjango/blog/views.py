from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from . forms import *
from core.models import *

def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return render(request, 'blog/home.html')
        else:
            if request.method == 'POST':

                filterAtt = request.POST['filter1']
                if filterAtt:
                    if filterAtt == "veg":
                        filter_qs = Item.objects.filter(is_veg=True, chef = request.user)
                        return render(request, 'blog/chef_home.html',context={'items' : filter_qs})
                    elif filterAtt == "nonveg":
                        filter_qs = Item.objects.filter(is_veg=False, chef = request.user)
                        return render(request, 'core/chef_home.html',context={'items' : filter_qs})


                filterAtt = request.POST['filter2']
                if filterAtt:
                    if filterAtt == "lte100":
                        filter_qs = Item.objects.filter(price__range=(0,100), chef = request.user)
                        return render(request, 'core/chef_home.html',context={'items' : filter_qs})
                    elif filterAtt == "100to200":
                        filter_qs = Item.objects.filter(price__range=(101,199), chef = request.user)
                        return render(request, 'core/chef_home.html',context={'items' : filter_qs})
                    elif filterAtt == "gte200":
                        filter_qs = Item.objects.filter(price__range=(200,1000), chef = request.user)
                        return render(request, 'core/chef_home.html',context={'items' : filter_qs})

                sortAtt = request.POST['sort']
                if sortAtt:
                    if sortAtt == "priceAsc":
                        sorted_qs = Item.objects.filter(chef = request.user).order_by('price')
                        return render(request, 'core/chef_home.html',context={'items' : sorted_qs})
                    elif sortAtt == "priceDesc":
                        sorted_qs = Item.objects.order_by('-price')
                        return render(request, 'core/chef_home.html',context={'items' : sorted_qs})

            return render(request, 'blog/chef_home.html', context={'items' : Item.objects.filter(chef = request.user).all()})


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
