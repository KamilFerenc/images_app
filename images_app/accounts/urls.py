from django.conf.urls import url

from images_app.accounts.views import user_detail_api_view

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', user_detail_api_view, name='detail')
]
