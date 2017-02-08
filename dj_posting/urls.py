from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from photos.views import PhotosList, PhotosDetail


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', PhotosList.as_view(), name='photos_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
