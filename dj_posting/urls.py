from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from photos.views import PhotosListView, like_add_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', PhotosListView.as_view(), name='photos_list_all'),
    url(r'^like/(?P<photo_id>\d+)$', like_add_view, name='like_add'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
