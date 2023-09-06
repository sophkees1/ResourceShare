from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Count, Avg

from .models import Resources, Tag, Review, Rating
from apps.user.models import User
from .utils import generate_cat_count_list



def home_page(request):
    cnt = Resources.objects.all().count()
    users_cnt = User.objects.filter(is_active=True).count()
    res_per_cat = Resources.objects.values("cat_id__cat").annotate(cnt=Count("cat_id"))
    
    context = {
        "cnt": cnt,
        "users_cnt": users_cnt,
        "res_per_cat": res_per_cat
    }
    
    return render(
        request=request, 
        template_name="resources/home.html", 
        context=context
        )




def resource_detail(request, id):
    res = Resources.objects.select_related("user_id", "cat_id").get(pk=id)
    tags = Tag.objects.filter(resources=res)
    tag_names = ", ".join([tag.name for tag in tags])
    reviews_cnt = Review.objects.filter(resources_id=res).count()
    average_rating = Rating.objects.filter(resources_id=res).aggregate(avg_rating=Avg("rate"))["avg_rating"]
    
    context = {
        "res": res,
        "tags": tags,
        "tag_names": tag_names,
        "reviews_cnt": reviews_cnt,
        "average_rating": average_rating
    }
    
    return render(
        request=request,
        template_name="resources/resource_detail.html",
        context=context
    )







################################################################

# function base view
def home_page_old(request):
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



def resource_detail_old(request, id):
    res = Resources.objects.select_related("user_id", "cat_id").get(pk=id)
    tags = Tag.objects.filter(resources=res)
    tag_names = ", ".join([tag.name for tag in tags])
    response = f"""
        <html>
            <h1 style="color: blue">Resource: {res.title}</h1>
            <p><b>User:</b> {res.user_id.username}</p>
            <a href="{res.link}"><b>Link To The Video</b></a>
            <p><b>Description:</b> {res.description}</p>
            <p><b>Category:</b> {res.cat_id.cat}</p>
            <p><b>Tags:</b> {tag_names}</p>
        </html>
    """
    return HttpResponse(response)


# class base view
# class HomePage(TemplateView):
#     template_name = "home_page.html"


