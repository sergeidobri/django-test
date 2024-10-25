from django.contrib import admin, messages
from .models import Nails, Category
from django.utils.safestring import mark_safe


class CreatedFilter(admin.SimpleListFilter):
    title = 'Создатель'
    parameter_name = 'created'

    def lookups(self, request, model_admin):
        return [
            ('known', 'Известный создатель'),
            ('unknown', 'Неизвестный создатель'),
        ]

    def queryset(self, request, queryset):
        if self.value() == "known":
            return queryset.filter(creator__isnull=False)
        elif self.value() == 'unknown':
            return queryset.filter(creator__isnull=True)

@admin.register(Nails)
class NailsAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'show_photo', 'slug', 'cat', 'tags']
    filter_horizontal = ['tags']
    readonly_fields = ['show_photo']
    list_display = ('title', 'show_photo', 'time_create', 'time_update', 'is_available', 'cat')
    ordering = ['title']
    list_display_links = ('title', )
    list_editable = ('is_available',)
    actions = ['set_available', 'set_draft']
    search_fields = ('title', 'cat__name')
    list_filter = (CreatedFilter, 'cat__name', 'is_available')
    save_on_top = True

    @admin.display(description='Показ изображения')
    def show_photo(self, nails: Nails):
        if nails.photo:
            return mark_safe(f'<img src="{nails.photo.url}" width=50>')
        return 'Без фото'

    @admin.display(description='Краткая информация')
    def brief_info(self, nail):
        return f'Описание {len(nail.content)} символов'

    @admin.action(description='Установить значение "Доступно"')
    def set_available(self, request, queryset):
        count = queryset.update(is_available=Nails.Status.AVAILABLE)
        self.message_user(request, f'{"Изменена" if count == 1 else "Изменено"} {count} {"запись" if count == 1 else ("записи" if 1 < count < 5 else "записей")}')

    @admin.action(description='Установить значение "Недоступно"')
    def set_draft(self, request, queryset):
        count = queryset.update(is_available=Nails.Status.DRAFT)
        self.message_user(request, f'{"Изменена" if count == 1 else "Изменено"} {count} {"запись" if count == 1 else ("записи" if 1 < count < 5 else "записей")}', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ('slug', )
