from django.views.generic import ListView

from .models import Photo, Tag


class PhotosListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'all_photos'
    paginate_by = 20

    def get_ordering(self):
        default_ordering = 'id'
        ordering = self.request.GET.get('order_by', default_ordering)
        return default_ordering

    def tags_session_update(self):
        include_tag_id = self.request.GET.get('include')
        if include_tag_id:
            included = self.request.session.get('include', [])
            included.append(include_tag_id)
            self.request.session['include'] = included

        exclude_tag_id = self.request.GET.get('exclude')
        if exclude_tag_id:
            excluded = self.request.session.get('exclude', [])
            excluded.append(exclude_tag_id)
            self.request.session['exclude'] = excluded

        if 'reset' in self.request.GET:
            self.request.session['include'] = []
            self.request.session['exclude'] = []

    def get_filter_tag_id(self):
        includes_ids = set(self.request.session.get('include', []))
        excludes_ids = set(self.request.session.get('exclude', []))
        return includes_ids - excludes_ids

    def get_queryset(self):
        self.tags_session_update()
        filter_ids = self.get_filter_tag_id()
        if filter_ids:
            queryset = Photo.objects.filter(id__in=filter_ids)
        else:
            queryset = Photo.objects.all()

        ordering = self.get_ordering()
        queryset = queryset.order_by(ordering).filter(is_hide=False)
        return queryset

    def get_context_data(self, **kwargs):
        # post_like_key = self.object.get_photo_key()
        # if self.request.session.get(post_like_key, 'False') == 'False':
        #     self.request.session[post_like_key] = 'True'
        #     self.object.add_like()

        context = super(PhotosListView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(is_hide=False)
        context['tags'] = tags
        return context
