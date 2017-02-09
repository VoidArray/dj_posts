from django.views.generic import ListView
from django.http import JsonResponse

from .models import Photo, Tag


class PhotosListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'all_photos'
    paginate_by = 20

    def order_session_update(self):
        default_ordering = 'id'
        ordering = self.request.GET.get('order_by')
        if ordering == 'date':
            ordering = 'creation_date'
        elif ordering == 'like':
            pass
        else:
            ordering = default_ordering
        self.request.session['ordering'] = ordering

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

    def get_queryset(self):
        self.tags_session_update()
        self.order_session_update()

        queryset = super(PhotosListView, self).get_queryset()

        includes_ids = self.request.session.get('include', [])
        if includes_ids:
            queryset = queryset.filter(tags__in=includes_ids)

        excludes_ids = self.request.session.get('exclude', [])
        if excludes_ids:
            queryset = queryset.exclude(tags__in=excludes_ids)

        ordering = self.request.session.get('ordering', 'id')
        if ordering == 'like':
            queryset = sorted(queryset, key=lambda p: p.like_count, reverse=True)
        else:
            queryset = queryset.order_by(ordering).filter(is_hide=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhotosListView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(is_hide=False)
        context['tags'] = tags
        return context


def like_add_view(request, photo_id):
    scored_photo = Photo.objects.filter(id=photo_id).first()
    if scored_photo:
        post_like_key = scored_photo.get_photo_key()
        if request.session.get(post_like_key, 'False') == 'False':
            request.session[post_like_key] = 'True'
            scored_photo.add_like()
    return JsonResponse({})
