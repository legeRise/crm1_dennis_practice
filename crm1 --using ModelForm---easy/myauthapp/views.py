from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .decorators import already_logged_in
from .forms import RegisterForm

# Create your views here.

@already_logged_in
def registerUser(request):
    registerform = RegisterForm()
    if request.method == 'POST':
            registerform = RegisterForm(request.POST)
            if registerform.is_valid():
                registerform.save() 

                messages.success(request,"Registration Successful...")
                return redirect('login')

    context = {'form':registerform}
    return render(request,'myauthapp/register.html',context)

@already_logged_in
def loginUser(request):
    if request.method == "POST":
         username =request.POST.get('username')
         password =request.POST.get('password')

         # check if user exists               
         user = authenticate(username=username,password=password)
         if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully...")
            
            user_groups =[group.name for group in request.user.groups.all()]
            if 'adminGroup' in user_groups:
                return redirect('dashboard')
            else:
                return redirect('UserDashboard')
            
         else:
            messages.error(request,"Incorrect Username or Password...",extra_tags='error')
              
         
    return render(request,'myauthapp/login.html')



def logoutUser(request):
     logout(request)
     return redirect('login')