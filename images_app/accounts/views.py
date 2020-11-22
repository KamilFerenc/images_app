from django.core.cache import cache
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from images_app.accounts.models import CustomUser
from images_app.accounts.permissions import IsOwner
from images_app.accounts.serializers import CustomUserSerializer


class UserDetailApiView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwner]
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        if response := cache.get(request.user.username):
            return Response(*response)
        response = super().get(request, *args, **kwargs)
        data, status_code = response.data, response.status_code
        cache.set(request.user.username, (data, status_code))
        return Response(data, status_code)


user_detail_api_view = UserDetailApiView.as_view()
