from django.shortcuts import render,redirect
from .models import Product,Order,Customer
from .forms import OrderForm,CustomerForm
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from .decorators import allowed_groups
# Create your views here.


@login_required(login_url='login')
@allowed_groups(['adminGroup'])
def home(request):
    all_customers = Customer.objects.all()
    # all order data for generating status_report
    all_orders = Order.objects.all()
    #status_report
    total_order_count = all_orders.count() # you also use len(all_orders)
    orders_delivered= all_orders.filter(status='Delivered').count()
    orders_pending= all_orders.filter(status='Pending').count()
    orders_on_the_way = all_orders.filter(status='On the Way').count()

    last_5_orders = all_orders.order_by('-date_created')[:5]

    content ={
        'all_customers':all_customers,'last_5_orders':last_5_orders,
        'status_report':
        {
            'total_order_count':total_order_count,
            'delivered':orders_delivered,
            'pending':orders_pending,'on_the_way':orders_on_the_way
        }
    }
    return render(request,'accounts/adminDashboard.html',content)






@login_required(login_url='login')
@allowed_groups(['adminGroup','customerGroup'])
def user(request):
    customer = request.user.customer
    print(customer.id)
    # all order data of the customer-for generating status_report
    all_orders = customer.order_set.all()
    #status_report
    total_order_count = all_orders.count() # you also use len(all_orders)
    orders_delivered= all_orders.filter(status='Delivered').count()
    orders_pending= all_orders.filter(status='Pending').count()
    orders_on_the_way = all_orders.filter(status='On the Way').count()

    last_5_orders = all_orders.order_by('-date_created')[:5]

    content ={
        'last_5_orders':last_5_orders,
        'status_report':
        {
            'total_order_count':total_order_count,
            'delivered':orders_delivered,
            'pending':orders_pending,'on_the_way':orders_on_the_way
        }
    }
    return render(request,'accounts/userDashboard.html',content)


@login_required(login_url='login')
@allowed_groups(['customerGroup','adminGroup'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        print(request.FILES)
        form = CustomerForm(request.POST,request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context ={'form':form}
    return render(request,'accounts/account_settings.html',context)






@login_required(login_url='login')
@allowed_groups(['adminGroup'])
def products(request):

    all_products =  Product.objects.all()
    context ={'all_products':all_products}

    return render(request,'accounts/products.html',context)




@login_required(login_url='login')
def customer(request,pk): #pk is dynamic value coming from urls
     customer = Customer.objects.get(id=pk)
     orders = customer.order_set.all()#same as Order.objects.filter(id=pk)
     order_count = customer.order_set.all().count() # or ofcourse orders.count()

     # adding an order filter
     myFilter  = OrderFilter(request.GET,queryset=orders)
     orders = myFilter.qs
     
     context={'customer':customer,'all_orders':orders,'count':order_count,'myFilter':myFilter}

     return render(request,'accounts/customer.html',context)




@login_required(login_url='login')
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    myform = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        myform = OrderForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('customer',pk=pk)
    context= {'myform':myform}     
    return render(request,'accounts/order.html',context)





@login_required(login_url='login')
def updateOrder(request,pk):
    requested_order = Order.objects.get(id=pk)
    customer = requested_order.customer
    myform =OrderForm(instance=requested_order)

    if request.method == 'POST':
        myform = OrderForm(request.POST,instance=requested_order)
        if myform.is_valid():
            myform.save()
            return redirect('customer',pk=customer.id)

    context= {'myform':myform}
    return render(request,'accounts/order.html',context)





@login_required(login_url='login')
def deleteOrder(request,pk):
    requested_order = Order.objects.get(id=pk)
    customer = requested_order.customer
    if request.method == 'POST':
        requested_order.delete()
        return redirect('customer',pk=customer.id)

    context= {'order':requested_order}
    return render(request,'accounts/delete_order.html',context)


