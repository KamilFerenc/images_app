from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from images_app.accounts.models import CustomUser
from images_app.accounts.serializers import CustomUserSerializer


class UserDetailApiView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()


user_detail_api_view = UserDetailApiView.as_view()

