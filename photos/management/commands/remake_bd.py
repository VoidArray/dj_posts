import random
import requests
from datetime import datetime

from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from photos.models import Photo, Tag


class Command(BaseCommand):


    def _drop_base(self):
        Tag.objects.all().delete()
        Photo.objects.all().delete()
        print('all deleted')

    def _create_tags(self):
        with open('photos/management/commands/tags.txt', 'r') as fh:
            for line in fh:
                new_tag = Tag(
                    title=line.strip()
                )
                new_tag.save()
        print('tags created, count: ', Tag.objects.count())

    def _create_photos(self):
        # print(os.getcwd())
        with open('photos/management/commands/test-photo.csv', 'r') as fh:
            next(fh)
            for line in fh:
                image_url, dt = line.split(';')[1:3]
                image_url = image_url[1:-1]
                dt = dt.strip()[1:-1]
                photo_dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

                r = requests.get(image_url, stream=True)
                if r.status_code != requests.codes.ok:
                    continue

                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(r.content)
                img_temp.flush()

                file_name = image_url.rsplit('/', 1)[1]
                tags_count = random.randint(4, 7)

                new_photo = Photo()
                new_photo.creation_date = photo_dt
                new_photo.image.save(file_name, File(img_temp), save=True)
                new_photo.tags = Tag.objects.order_by('?')[:tags_count]
                new_photo.save()
                print('\t', file_name)

        print('photos loaded, count: ', Photo.objects.count())


    def handle(self, *args, **options):
        self._drop_base()
        self._create_tags()
        self._create_photos()
