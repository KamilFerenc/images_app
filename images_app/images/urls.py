from django.conf.urls import url

from images_app.images.views import add_image_api_view, generate_temporary_link, temporary_image_view

urlpatterns = [
    url(r'^add/$', add_image_api_view, name='add_image'),
    url(r'^generate-link/$', generate_temporary_link, name='generate_link'),
    url(r'(?P<link_suffix>.+)', temporary_image_view, name='temporary_image')
]
