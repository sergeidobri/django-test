from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=Nails.Status.AVAILABLE)
    

class Nails(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Недоступно'
        AVAILABLE = 1, 'Доступно'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг',
                            validators=[
                                MinLengthValidator(5),
                                MaxLengthValidator(100),
                            ])
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Контентыч')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_available = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Доступен')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='types', verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    creator = models.OneToOneField('Creator', on_delete=models.SET_NULL, null=True, blank=True, related_name='creation')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)

    objects = models.Manager()
    available = AvailableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известные маникюры'
        verbose_name_plural = 'Известные маникюры'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug_id': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Имя категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Creator(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    c_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
