from typing import Optional
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User


# Create your views here.
def user_list(request):
    users = User.objects.all()
    
    context = {
        "users": users
    }
    return render(
        request=request,
        template_name="user/user_list.html",
        context=context
    )


def login_view(request):
    error_message = None
    
    # Unbound state of our form
    form = AuthenticationForm()
    
    if request.method == 'POST':
        # Bound state of our form
        form = AuthenticationForm(data=request.POST)
        
        # validate the data
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            # authenticate the user
            user: Optional[User] = authenticate(
                username=username, 
                password=password
            )
            
            # check if user was authenticated
            if user is not None:
                # use the session to keep the authenticated users' id
                login(request, user)
                # when we login, the session will store the user id
                # the authentication middleware is going to use that id
                # and fetch the user from the database and store it in the 
                # request.user object

                
                # redirect the user to their profile page
                return redirect("profile")
            
            # TODO: if user is not authenticated what should you do?
            
        else:
            # users data is not valid. so set an error message to be displayed
            error_message = "Sorry, something went wrong. Please try again."
    
    context = {"form": form, "error_message": error_message}
    
    return render(request, "user/login.html", context)   
            

def logout_view(request):
    logout(request)
    
    return redirect(login_view)

@login_required  
def profile(request):
    return render(
        request, 
        "user/profile.html"
    )
    
