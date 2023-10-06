from rest_framework.exceptions import PermissionDenied

DEFAULT_CATEGORY_ID = 2

# <idea>mixin

class DenyDeletionOfDefaultCategoryMixin():
    # we want to get the cat id we are about to delete
    # we want to compare it with the DEFAULT_CATEGORY_ID
    # if true, raise an exception.
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "destroy":
            pk = self.kwargs["pk"]
            deleted_queryset = queryset.get(pk=pk)
            if deleted_queryset.id == DEFAULT_CATEGORY_ID:
                raise PermissionDenied(
                    f"Not allowed to delete category with id {pk}"
                )
        return queryset

class FilterOutAdminResourcesMixin():
    def get_queryset(self):
        queryset = super().get_queryset().exclude(user_id__is_superuser__exact=True)
        return queryset
    

class FilterByCategoryMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params
        
        category = query_params.get("cat")
        if category:
            return queryset.filter(cat_id__cat__iexact=category)
        else:
            return queryset