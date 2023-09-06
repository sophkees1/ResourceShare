from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import CreatedModifiedDatetimeBase
from apps.resources import validators
# Create your models here.


class Tag(CreatedModifiedDatetimeBase):
    # id=None if you dont want the default id to be created
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Category(CreatedModifiedDatetimeBase):
    cat = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.cat
    
    
class Resources(CreatedModifiedDatetimeBase):
    user_id = models.ForeignKey(
        "user.User", null=True, on_delete=models.SET_NULL
    )
    cat_id = models.ForeignKey(
        "resources.Category", default=1, on_delete=models.SET_DEFAULT
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=500)
    tags = models.ManyToManyField("resources.Tag", through="ResourcesTag")
    
    #rate = ArrayField(base_field=models.IntegerField()) # INT ARRAY
    
    class Meta:
        verbose_name_plural = "Resources"
    
    def __str__(self):
        return f"{self.user_id.username} - {self.title}"
    
    def user_title(self):
        return self.user_id.title
    
    def all_tags(self):
        return ", ".join([tag.name for tag in self.tags.all()])
    
    
    
class ResourcesTag(CreatedModifiedDatetimeBase):
    modified_at = None
    resources_id = models.ForeignKey("resources.Resources", on_delete=models.CASCADE)
    tag_id = models.ForeignKey("resources.Tag", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.resources_id.title} - {self.tag_id.name}"

    def title(self):
        return self.resources_id.title

    def tag(self):
        return self.tag_id.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "resources_id",
                "tag_id",
                name="resource_tag_unique",
                violation_error_message="Tag already exists for resource"
            )
        ]
    
    
class Review(CreatedModifiedDatetimeBase):
    user_id = models.ForeignKey(
        "user.User", null=True, on_delete=models.SET_NULL
    )
    resources_id = models.ForeignKey("resources.Resources", on_delete=models.CASCADE)
    body = models.TextField()
    
    def __str__(self):
        return f"{self.user_id.username} - {self.resources_id.title}"
    
    def username(self):
        return self.user_id.username

    def title(self):
        return self.resources_id.title

    
    
class Rating(CreatedModifiedDatetimeBase):
    user_id = models.ForeignKey(
        "user.User", null=True, on_delete=models.SET_NULL
    )
    resources_id = models.ForeignKey("resources.Resources", on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[validators.check_rating_range])
    
    def __str__(self):
        return str(self.rate)

    def username(self):
        return self.user_id.username

    def title(self):
        return self.resources_id.title
