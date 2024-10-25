from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.NailShow.as_view(), name="home"),
    path('about/', views.about, name='about'),
    path('post/<slug:slug_id>/', views.ShowPost.as_view(), name='post'),
    path('add/', views.AddInstruction.as_view(), name='add'),
    path('order/', views.order, name='order'),
    path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>', views.NailsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.NailsTags.as_view(), name='tag'),
    path('edit/<int:pk>', views.UpdateInstruction.as_view(), name='edit_page'),
    path('delete/<int:pk>', views.DeleteInstruction.as_view(), name='delete_page'),
]
