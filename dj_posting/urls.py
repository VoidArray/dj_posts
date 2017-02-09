from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from photos.views import PhotosListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', PhotosListView.as_view(), name='photos_list_all'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
