from django.shortcuts import redirect

def already_logged_in(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return func(request,*args,**kwargs)
    return wrapper

