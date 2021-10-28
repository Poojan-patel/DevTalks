from django.contrib import messages
from django.shortcuts import redirect

def errorView(request):
     #messages.error(request,"Request Page not Exists")
     messages.warning(request,"Requested Page not Exists, Redirected to Home")
     #messages.info(request,"Redirected to Feed")
     return redirect('feed')