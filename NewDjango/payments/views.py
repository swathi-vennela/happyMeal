from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from core.models import Order,OrderedList
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

global user

def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'payments/pay.html')
    # try:
    # username = request.POST['username']
    # password = request.POST['password']
    global user 
    user = request.user
    amount = Order.objects.get(user=request.user, ordered=False).get_total();
    #     user = authenticate(request, username=username, password=password)
    #     if user is None:
    #         raise ValueError
    #     auth_login(request=request, user=user)
    # # except:
    #     return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=request.user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    
    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        global user
        order = Order.objects.get(user=user, ordered=False)
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
            for order_item in order.items.filter(ordered = False).all():
                order_item.set_change_order_status()
                # item = get_object_or_404(Item, slug=slug)
                # ordered_list, created = OrderedList.objects.get_or_create(chef= order_item.item.get_chef())
                order_qs = OrderedList.objects.filter(chef= order_item.item.get_chef())
                if order_qs.exists():
                    order = order_qs[0]
                #check if the order item is in the order
                    order.items.add(order_item)
                else:
                    
                    order = OrderedList.objects.create(chef= order_item.item.get_chef())
                    order.items.add(order_item)


                mail_subject = 'Payment receipt.'
                message = render_to_string('payments/callback.html', context=received_data)
                plain_message = strip_tags(message)
                to_email = user.email
                email = EmailMessage(
                    mail_subject, plain_message, to=[to_email]
                )
                email.send()
    
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        return render(request, 'payments/callback.html', context=received_data)




