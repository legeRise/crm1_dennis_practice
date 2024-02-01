from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Order,Customer
# Create your views here.



def home(request):

    all_customers = Customer.objects.all()

    # all order data for generating status_report
    all_orders = Order.objects.all()
    #status_report
    total_order_count = all_orders.count() # you also use len(all_orders)
    orders_delivered= all_orders.filter(status='Delivered').count()
    orders_pending= all_orders.filter(status='Pending').count()
    orders_on_the_way = all_orders.filter(status='On the Way').count()


    total = len(list(all_orders))-1 # -1 bcz index from 0
    last_5_orders = all_orders[total:total-5:-1] 

    last_5_orders = all_orders.order_by('-date_created')[:5]


    content ={
        'all_customers':all_customers,'last_5_orders':last_5_orders,
        'status_report':
        {
            'total_order_count':total_order_count,'delivered':orders_delivered,
            'pending':orders_pending,'on_the_way':orders_on_the_way
        }
    }
    
    return render(request,'accounts/dashboard.html',content)
    

def products(request):

    all_products =  Product.objects.all()
    context ={'all_products':all_products}

    return render(request,'accounts/products.html',context)

  
def customer(request,pk): #pk is dynamic value coming from urls
     customer = Customer.objects.get(id=pk)
     orders = customer.order_set.all()#same as Order.objects.filter(id=pk)
     order_count = customer.order_set.all().count() # or ofcourse orders.count()
     
     context={'customer':customer,'all_orders':orders,'count':order_count}

     return render(request,'accounts/customer.html',context)


"""  WHEN DONE MANUALLY   ---- without using django forms  """
def createOrder(request):

    all_customers = Customer.objects.all()
    all_products = Product.objects.all()
    #status_types
    status_types = [(value,status_text) for value,status_text in Order.STATUS]

    if request.method == 'POST':
        customer=request.POST.get('customer')
        customer = all_customers.get(id=customer)

        product=request.POST.get('product')
        product= all_products.get(id=product)

        status=request.POST.get('status')
        
        new_order = Order(customer=customer,product=product,status=status)
        new_order.save()
        return redirect('dashboard')


    context= {'customers':all_customers,'products':all_products,'status_types':status_types}
        
    return render(request,'accounts/order.html',context)



def updateOrder(request,pk):

    all_customers = Customer.objects.all()
    all_products = Product.objects.all()
    #status_types
    status_types = [(value,status_text) for value,status_text in Order.STATUS]

    if request.method == 'POST':
        customer=request.POST.get('customer')
        customer = all_customers.get(id=customer)

        product=request.POST.get('product')
        product= all_products.get(id=product)

        status=request.POST.get('status')

        update_order = Order.objects.get(id=pk)
        update_order = Order(id=pk,customer=customer,product=product,status=status)
        update_order.save()
        return redirect('customer',pk=customer.id)


    context= {'customers':all_customers,'products':all_products,'status_types':status_types}
        
    return render(request,'accounts/order.html',context)



def deleteOrder(request,pk):

    order = Order.objects.get(id=pk)
    if request.method == 'POST':

        order.delete()
        return redirect('dashboard')


    context= {'order':order}
        
    return render(request,'accounts/delete_order.html',context)

    

""" ----   WHEN DONE MANUALLY   ----   """
