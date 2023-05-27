from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('posts',views.AllPostsView.as_view(),name="posts"),
    path('posts/<slug:slug>',views.PostDetailView.as_view(),name="post_detail"),
    path('favorites/',views.AddFavoriteView.as_view(),name="favorites"),
    path('remove-favorites/<int:id>',views.RemoveFavoriteView.as_view(),name="remove-favorites"),
    path('author/<str:name>',views.AuthorDetailView.as_view(),name="author_detail"),
    path('tag/<str:captions>',views.TagDetailView.as_view(),name="tag_detail")
]
