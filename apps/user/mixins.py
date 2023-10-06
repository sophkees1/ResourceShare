from . import serializers

class RestrictInactiveUsersMixin:
    def get_serializer_class(self):
        if self.request.user.is_active:
            return serializers.UserUpdateModelSerializer
        else:
            return serializers.UserModelSerializer