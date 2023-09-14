from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required

from .models import Resources, Tag, Review, Rating
from apps.user.models import User
from .utils import generate_cat_count_list
from .form import PostResourceForm


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



@login_required
def resource_detail(request, id):
    max_viewed_resources = 5
    
    viewed_resources = request.session.get("viewed_resources", [])
    
    res = Resources.objects.select_related("user_id", "cat_id").get(pk=id)
    tags = Tag.objects.filter(resources=res)
    tag_names = ", ".join([tag.name for tag in tags])
    reviews_cnt = Review.objects.filter(resources_id=res).count()
    average_rating = Rating.objects.filter(resources_id=res).aggregate(avg_rating=Avg("rate"))["avg_rating"]
    
    # prepare our data
    viewed_resource = [id, res.title]
    
    # check if that data exists already and remove it
    if viewed_resource in viewed_resources:
        viewed_resources.remove(viewed_resource)
    
    # add it as first item
    viewed_resources.insert(0, viewed_resource)
    
    # Get limit
    viewed_resources = viewed_resources[:max_viewed_resources]
    
    # add it back in the session
    request.session["viewed_resources"] = viewed_resources
    
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

@login_required
def resource_post(request):
    #Unbound- User made a GET request
    if request.method == "GET":
        form = PostResourceForm()  
        return render(
            request,
            "resources/resource_post.html",
            {"form": form}
        )
    else:
        # Bound- User made a POST request
        form = PostResourceForm(request.POST)
        # validation
        # .is_valid() method
        # .cleaned_data attribute
        if form.is_valid():
            new_data = form.cleaned_data
            new_data["user_id_id"] = 1
            resource = Resources.objects.create(
                user_id_id=new_data["user_id_id"],
                cat_id_id=new_data["category"], 
                title=new_data["title"],
                description=new_data["description"],
                link=new_data["link"],
            )
            # Create a list of selected tag IDs
            tag_ids = new_data.get("tags", []) 
            # Associate the selected tags with the resource
            resource.tags.set(tag_ids)
            
            return redirect(home_page)
        



################################################################this is old and was for practice purposes

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


