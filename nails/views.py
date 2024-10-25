from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Nails, TagPost
from .forms import AddInstructionForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


class NailShow(DataMixin, ListView):
    model = Nails
    template_name = 'nails/index.html'
    cat_selected = 0
    context_object_name = 'nails'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Nails.available.all().select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Nails
    template_name = 'nails/post.html'
    slug_url_kwarg = 'slug_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Nails.available, slug=self.kwargs[self.slug_url_kwarg])


class AddInstruction(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddInstructionForm
    template_name = 'nails/add.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавить инструкцию'
    permission_required = 'nails.add_nails'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdateInstruction(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Nails
    fields = '__all__'
    template_name = 'nails/add.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование страницы'
    permission_required = 'nails.change_nails'


class DeleteInstruction(DataMixin, DeleteView):
    model = Nails
    template_name = 'nails/delete_post.html'
    success_url = reverse_lazy("home")
    title_page = 'Удаление страницы'


class NailsCategory(DataMixin, ListView):
    template_name = 'nails/index.html'
    context_object_name = 'nails'
    allow_empty = False

    def get_queryset(self):
        return Nails.available.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['nails'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


class NailsTags(DataMixin, ListView):
    template_name = 'nails/index.html'
    context_object_name = 'nails'
    allow_empty = False

    def get_queryset(self):
        return TagPost.objects.get(slug=self.kwargs['tag_slug']).tags.filter(is_available=Nails.Status.AVAILABLE).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug']).tag
        return self.get_mixin_context(context, title=f'Тег: {tag}')
