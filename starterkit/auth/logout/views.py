from django.contrib.auth import logout
from django.shortcuts import redirect

def LogOutView(request):
    logout(request)  # This logs out the user
    return redirect('/')  # Redirects to the homepage after logout
