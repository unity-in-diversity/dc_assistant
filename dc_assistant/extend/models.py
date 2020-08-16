from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from taggit.models import TagBase, GenericTaggedItemBase
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from extend.forms import ColorField

__all__ = (
    'Tag',
    'TaggedItem',
    'ImgAttach')

class Tag(TagBase):

    color = ColorField(
        default='9e9e9e'
    )
    comments = models.TextField(
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def get_absolute_url(self):
        return reverse('extend:tag', args=[self.slug])

    def slugify(self, tag, i=None):
        slug = slugify(tag, allow_unicode=True)
        if i is not None:
            slug += "_%d" % i
        return slug

class TaggedItem(GenericTaggedItemBase):

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    # class Meta:
    #     index_together = (("content_type", "object_id"))


def img_upload(instance, filename):
    """
    Преобразовываем, переименовываем с учтом объекта к которму относится картинка.
    """
    path = 'imgs-attachments/'
    extension = filename.rsplit('.')[-1].lower()
    if instance.name and extension in ['bmp', 'gif', 'jpeg', 'jpg', 'png']:
        filename = '.'.join([instance.name, extension])
    elif instance.name:
        filename = instance.name

    return '{}{}_{}_{}'.format(path, instance.content_type.name, instance.object_id, filename)


class ImgAttach(models.Model):
    """
    Хранение картинок связанных с объектами различных моделей
    """
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id')

    image = models.ImageField(
        upload_to=img_upload,
        height_field='image_height',
        width_field='image_width')

    image_height = models.PositiveSmallIntegerField()
    image_width = models.PositiveSmallIntegerField()

    name = models.CharField(
        max_length=50,
        blank=True)

    created = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        ordering = ('name', 'pk')

    def __str__(self):
        if self.name:
            return self.name
        filename = self.image.name.rsplit('/', 1)[-1]
        return filename.split('_', 2)[2]


class LoggingModel(models.Model):
    created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
