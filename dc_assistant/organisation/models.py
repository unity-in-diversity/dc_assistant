from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
from extend.models import TaggedItem, ImgAttach, LoggingModel
from extend.forms import ColorField
from smart_selects.db_fields import ChainedForeignKey


#TODO: в url.py каждого приложения определить пространство уролов используемое в функциях get_absolute_url моделей

class Region(MPTTModel):
    """
    Регион/город, каждая созданная точка может быть родителем для другой
    """
    parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
        db_index=True)

    name = models.CharField(
        max_length=50,
        unique=True)

    slug = models.SlugField(
        unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?region={}".format(reverse('organisation:location_list'), self.slug)

class Location(LoggingModel):
    """
    Место расположения инфраструктуры (здание, офис, цод и т.п.)
    """
    name = models.CharField(
        max_length=50,
        unique=True)

    slug = models.SlugField(
        unique=True)

    region = models.ForeignKey(
        to=Region,
        on_delete=models.SET_NULL,
        related_name='locations',
        blank=True,
        null=True)

    physical_address = models.CharField(
        max_length=200,
        blank=True)

    description = models.CharField(
        max_length=100,
        blank=True)

    comment = models.TextField(
        blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organisation:location', args=[self.slug])

class Rack(LoggingModel):
    """
    Конфигурация стойки
    """
    TYPE_1FRAME = '1-frame'
    TYPE_2FRAME = '2-frame'
    TYPE_WALLCABINET = 'wall-cabinet'
    TYPE_FLOORCABINET = 'floor-cabinet'

    RACK_TYPE_CHOICES = (
        (TYPE_1FRAME, 'Открытая стойка однорамочная'),
        (TYPE_2FRAME, 'Открытая стойка двухрамочная'),
        (TYPE_WALLCABINET, 'Серверный шкаф настенный'),
        (TYPE_FLOORCABINET, 'Серверный шкаф напольный'),
        )

    name = models.CharField(
        max_length=50)

    location = models.ForeignKey(
        to=Location,
        on_delete=models.PROTECT,
        related_name='racks')

    u_height = models.PositiveSmallIntegerField(
        default=44,
        verbose_name='Unit Height',
        validators=[MinValueValidator(1), MaxValueValidator(100)])

    desc_units = models.BooleanField(
        default=False,
        verbose_name='Top to buttom',
        help_text='По умолчанию нумерация юнитов снизу вверх')

    racktype = models.CharField(
        max_length=50,
        choices=RACK_TYPE_CHOICES,
        default=TYPE_FLOORCABINET,)

    comment = models.TextField(
        blank=True)

    class Meta:
        ordering = ('location', 'name', 'pk')

    def __str__(self):
        return self.display_name or super().__str__()

    def get_absolute_url(self):
        return reverse('organisation:rack', args=[self.pk])

    @property
    def display_name(self):
        if self.location:
            return "{} ({})".format(self.name, self.location)
        elif self.name:
            return self.name
        return ""

    @property
    def units(self):
        if self.desc_units:
            return range(1, self.u_height + 1)
        else:
            return reversed(range(1, self.u_height + 1))


class Vendor(LoggingModel):
    """
    Представляет список производителей.
    """
    name = models.CharField(
        max_length=50,
        unique=True)

    slug = models.SlugField(
        unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?vendor={}".format(reverse('organisation:model_list'), self.slug)

class VendorModel(LoggingModel):
    """
    Представялет конкретные модели оборудования вендоров
    """
    vendor = models.ForeignKey(
        to=Vendor,
        on_delete=models.PROTECT,
        related_name='device_models')

    model = models.CharField(
        max_length=50)

    slug = models.SlugField()

    u_height = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Height (U)')

    depth = models.BooleanField(
        default=True,
        verbose_name='Full Depth',
        help_text='Default is Full Depth')

    front_image = models.ImageField(
        upload_to='imgs-devicemodel',
        blank=True)

    rear_image = models.ImageField(
        upload_to='imgs-devicemodel',
        blank=True)

    comment = models.TextField(
        blank=True)

    def get_absolute_url(self):
        return reverse('organisation:vendormodel', args=[self.pk])

    @property
    def display_name(self):
        return '{} {}'.format(self.vendor.name, self.model)


class Platform(LoggingModel):

    name = models.CharField(
        max_length=100,
        unique=True)

    slug = models.SlugField(
        unique=True,
        max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?platform={}".format(reverse('organisation:device_list'), self.slug)


class DeviceRole(LoggingModel):

    name = models.CharField(
        max_length=50,
        unique=True)

    slug = models.SlugField(
        unique=True)

    description = models.CharField(
        max_length=100,
        blank=True)

    color = ColorField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Device(LoggingModel):
    """
    Представление единиц оборудованиея со свойствами и связями
    """

    #TODO: добавить обьединение в кластер, генерация IP адресов

    FRONT = 1
    REAR = 0

    RACK_SIDE_CHOICES = (
        (FRONT, 'Размещено на лицевой стороне стойки'),
        (REAR, 'Размещено на обратной стороне стойки'),
    )

    #TODO: добавить выбор типа оборудования и поля с выбором

    name = models.CharField(
        max_length=50,
        unique=True)

    device_model = models.ForeignKey(
        to=VendorModel,
        on_delete=models.PROTECT,
        related_name='instances')

    device_role = models.ForeignKey(
        to=DeviceRole,
        on_delete=models.PROTECT,
        related_name='devices')

    platform = models.ForeignKey(
        to=Platform,
        on_delete=models.SET_NULL,
        related_name='devices',
        blank=True,
        null=True)

    serial = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Серийный номер')

    location = models.ForeignKey(
        to=Location,
        on_delete=models.PROTECT,
        related_name='devices')

    # rack = models.ForeignKey(
    #     to=Rack,
    #     on_delete=models.PROTECT,
    #     related_name='devices',
    #     blank=True,
    #     null=True)

    rack = ChainedForeignKey(
        Rack,
        chained_field='location',
        chained_model_field='location',
        related_name='devices',
        show_all=False,
        auto_choose=True,
        sort=True
    )

    position = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name='Номер юнита',
        help_text='Номер юнита с которого начинается размещение оборудование в стойке')

    face_position = models.PositiveSmallIntegerField(
        choices=RACK_SIDE_CHOICES,
        default=FRONT,
        blank=True,
        null=True)

#    cluster = models.ForeignKey(
#        to='Cluster',
#        on_delete=models.SET_NULL,
#        related_name='devices',
#        blank=True,
#        null=True)

#    primary_ip = models.OneToOneField(
#        to='IPAddress',
#        on_delete=models.SET_NULL,
#        related_name='primary_ip',
#        blank=True,
#        null=True,
#        verbose_name='Основной IP адрес')

    description = models.CharField(
        max_length=100,
        blank=True)

    comment = models.TextField(
        blank=True)

    images = GenericRelation(to=ImgAttach)

    tag = TaggableManager(through=TaggedItem)

    class Meta:
        ordering = ('name', 'pk')

    def __str__(self):
        return self.display_name or super().__str__()

    def get_absolute_url(self):
        return reverse('organisation:device', args=[self.pk])

