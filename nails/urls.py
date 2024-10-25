from django.urls import path
from . import views

urlpatterns = [
    path('', views.NailShow.as_view(), name="home"),
    path('post/<slug:slug_id>/', views.ShowPost.as_view(), name='post'),
    path('add/', views.AddInstruction.as_view(), name='add'),
    path('category/<slug:cat_slug>', views.NailsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.NailsTags.as_view(), name='tag'),
    path('edit/<int:pk>', views.UpdateInstruction.as_view(), name='edit_page'),
    path('delete/<int:pk>', views.DeleteInstruction.as_view(), name='delete_page'),
]
