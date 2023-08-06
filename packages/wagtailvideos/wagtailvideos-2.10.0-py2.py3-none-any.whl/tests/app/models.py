from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtailvideos.blocks import VideoChooserBlock
from wagtailvideos.models import AbstractVideo, AbstractVideoTranscode
from modelcluster.fields import ParentalKey


class CustomVideoModel(AbstractVideo):
    attribution = models.TextField(blank=True)

    admin_form_fields = (
        'title',
        'attribution',
        'file',
        'collection',
        'thumbnail',
        'tags',
    )


class CustomVideoTranscode(AbstractVideoTranscode):
    video = models.ForeignKey(CustomVideoModel, related_name='transcodes', on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('video', 'media_format')
        )


class TestPage(Page):
    video_field = models.ForeignKey(
        CustomVideoModel, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

    video_streamfield = StreamField([
        ('video', VideoChooserBlock())
    ], blank=True)

    content_panels = Page.content_panels + [
        VideoChooserPanel('video_field'),
        StreamFieldPanel('video_streamfield'),
    ]
