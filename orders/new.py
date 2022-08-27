
from datetime import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


from carts.models import CartItem
from django.http import HttpResponse
from .forms import OrderForm,PaymentMethodForm
from .models import Order, OrderProduct
from store.models import Product
import datetime

from django.http import HttpResponse

from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Payment


from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.



status=''  

def payments(request):
    store_id = settings.STORE_ID
    store_pass = settings.STORE_PASS
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id= store_id, sslc_store_pass=store_pass)
    
    status_url = request.build_absolute_uri(reverse('status'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    
    quantity = 0
    total =0
    grand_total = 0
    tax = 0
    order_details = Order.objects.filter(user = request.user , is_ordered=False)
    cart_items = CartItem.objects.filter(user = request.user)
    cart_count = cart_items.count()
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    # total = order_details.order_total
    tax = (2 * total)/100
    grand_total = total + tax 
   
    
    # print(order_details)
    # print(cart_items)
    # print(cart_count)
    # print(quantity)
    # print(grand_total)
    mypayment.set_product_integration(total_amount=Decimal(grand_total), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=cart_count, shipping_method='YES', product_profile='None')
    
    current_user = request.user
    user_details = Order.objects.filter(user = current_user)[0]
    # print(user_details.user.first_name)
    # print(user_details.user.email)
    # print(user_details.user.phone_number)
    full_name = user_details.user.first_name+ user_details.user.last_name
    # print(full_name)
    mypayment.set_customer_info(name=full_name, email= user_details.user.email, address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone= user_details.user.phone_number)
    
    billing_address = Order.objects.filter(user = request.user )[0]
    customer_name = billing_address.full_name()
    address_1 = billing_address.address_line_1
    city = billing_address.city
    country = billing_address.country
    
   
    mypayment.set_shipping_info(shipping_to=customer_name, address=address_1, city=city, postcode='1209', country=country)
    response_data = mypayment.init_payment()
    print(response_data['status'])
    status = response_data['status']
    print(status)
    return redirect(response_data['GatewayPageURL'])

    # return redirect('checkout')
    # return render(request,'orders/payment.html')
    
    
    
    
@csrf_exempt
def sslc_status(request):
    if request.method =='post' or request.method == 'POST':
        payment_data = request.POST
        # print(payment_data)
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            status = payment_data['status']
            print(status)
            return redirect(reverse('sslc_complete',kwargs={'val_id':val_id,'tran_id':tran_id}))
        else:
            print(payment_data)
    
    return render(request,'orders/status.html')
    
def sslc_complete(request,val_id,tran_id):
    # order = Order.objects.filter(user=request.user, is_ordered=False)  order_number=body['orderID']
    order = Order.objects.get(user=request.user, is_ordered=False )
    # print(order)
    # print(order.order_total)
   
     # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id =tran_id,
        payment_method = 'SSLCommerz',
        amount_paid =  order.order_total,
        # status = status,
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    # return redirect('home')

    # move the cart items to Order Product table 
    
    # order = Order.objects.get(user = request.user , is_ordered = True)
    
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        
        # orderproduct varications
        cart_item = CartItem.objects.get(id=item.id)
        product_variations = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variations)
        orderproduct.save()
    
        # Reduce the quantity of the sold products 
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
    
    # clear cart 
    CartItem.objects.filter(user = request.user).delete()
    # send order recieved email to customer 
    mail_subject = 'Thank you for your Order'
    message = render_to_string('orders/order_receieved_email.html',{
                'user':request.user,
                'order':order
               
                
            })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    # send the order number and transaction id back to sendData method 
    
    return redirect('home')
    

    
    







   
def place_order(request , total = 0 , quantity = 0):
    current_user = request.user
    
    # if the cart count is less than or equal to 0, then redirect back to shop 
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    
    if cart_count <= 0 :
        return redirect('store') 
    
    grand_total = 0
    tax = 0 
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2 * total)/100
    grand_total = total + tax 
    
    
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the information inside the table 
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # to get the user ip address 
            data.save()
            # generate the order _number 
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            print(order_number)
            data.order_number = order_number
            data.save()
            
            
            payment_method = PaymentMethodForm()
            order = Order.objects.get(user = current_user,is_ordered = False,order_number = order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
               
            }
            return render(request,'orders/payment.html',context)
        else:
            return redirect('checkout')
           
            
    
def order_complete(request):
    return render(request,'orders/order_complete.html')