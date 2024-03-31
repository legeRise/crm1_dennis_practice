from django.http import HttpResponse
from typing import List



def allowed_groups(allowed_groups:List[str]):
    def decorator(viewfunc):
        def wrapper(request,*args,**kwargs):
            user_groups =[group.name for group in request.user.groups.all()]
            ALLOWED_STATUS =  any([group in user_groups for group in allowed_groups])
            if ALLOWED_STATUS:
                return viewfunc(request,*args,**kwargs)
            return HttpResponse('you are not Authorized to View This Page')
        return wrapper
    return decorator