from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Nails, TagPost, UploadFiles
from .forms import AddInstructionForm, UploadFileForm
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .utils import DataMixin, menu_lst
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
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


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1> <a href='http://127.0.0.1:8000/'>Вернуться на главную</a>")


@login_required
def about(request):
    nails = Nails.objects.all()
    paginator = Paginator(nails, 3)

    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'nails/about.html', {'title': 'О сайте', 'page_obj': page_obj, 'menu': menu_lst})


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


def order(request):
    return render(request, 'nails/order.html', {'title':'Запись на ноготочки', 'menu': menu_lst})


def login(request):
    return render(request, 'nails/login.html', {'title':'Регистрация', 'menu': menu_lst})


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
