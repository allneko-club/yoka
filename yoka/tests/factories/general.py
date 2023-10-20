from pathlib import Path

import factory
from django.core.files.uploadedfile import SimpleUploadedFile

TESTS_DIR = Path(__file__).resolve(strict=True).parent.parent
MEDIA_DIR = TESTS_DIR / 'media'
img_file = MEDIA_DIR / 'test_image.jpg'


class SimpleUploadedFileFactory(factory.Factory):
    """"""

    class Meta:
        model = SimpleUploadedFile

    name = factory.Sequence(lambda n: 'test_image%d.jpg' % n)
    content = open(img_file, 'rb').read()
    content_type = 'image/jpg'


class TextFileFactory(factory.Factory):
    """"""

    class Meta:
        model = SimpleUploadedFile

    name = factory.Sequence(lambda n: 'test%d.txt' % n)
    content = b'test'


class ImageFileFactory(factory.Factory):
    """"""

    class Meta:
        model = SimpleUploadedFile

    name = factory.Sequence(lambda n: 'test_image%d.jpg' % n)
    content = open(img_file, 'rb').read()
    content_type = 'image/jpeg'
