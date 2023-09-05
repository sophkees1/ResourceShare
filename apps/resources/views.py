from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Count

from .models import Resources
from apps.user.models import User
from .utils import generate_cat_count_list
# Create your views here.

# function base view
def home_page(request):
    cnt = Resources.objects.all().count()
    users_cnt = User.objects.filter(is_active=True).count()
    res_per_cat = Resources.objects.values("cat_id__cat").annotate(cnt=Count("cat_id"))
    
    
    response = f"""
        <html>
            <h1 style="color: blue">Welcome to ResourceShare!</h1>
            
            <h2>Total Resources:</h2>
            <p>{cnt} resources and counting...</p>
            
            <h2>Total Active Users:</h2>
            <p>{users_cnt} current active users and counting...</p>
            <br/>
            
            <h2 style="color: blue"><u>Resources per Category:</u></h2>
            <ol>
                {generate_cat_count_list(res_per_cat)}
            </ol>
        </html>
    """
    
    return HttpResponse(response)



# class base view
# class HomePage(TemplateView):
#     template_name = "home_page.html"


