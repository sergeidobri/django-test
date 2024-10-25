from django import forms
from .models import Category, Creator, Nails
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.validators import ValidationError

@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только русские символы'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddInstructionForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    creator = forms.ModelChoiceField(queryset=Creator.objects.all(), empty_label='Создатель неизвестен', label='Создатель', required=False)

    class Meta:
        model = Nails
        fields = ['title', 'slug', 'photo' ,'content', 'is_available', 'creator', 'tags', 'cat']
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-input'}),
            "content": forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URLыч'}


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')
