from django.views.generic import ListView, DetailView

from .models import Photo, Tag


class PhotosList(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'all_photos'

    def get_queryset(self):
        queryset = Photo.objects.all()
        return queryset


class PhotosDetail(DetailView):
    model = Photo
    template_name = 'photos/post_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        post_like_key = self.object.get_photo_key()
        if self.request.session.get(post_like_key, 'False') == 'False':
            self.request.session[post_like_key] = 'True'
            self.object.add_like()

        context = super(PhotosDetail, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = tags
        return context
