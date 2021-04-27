from django.urls import path
from . views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, SignUpView, LoginView
from . views import LogoutView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('logout/', LogoutView, name="logout"),
    path('login/', LoginView, name="login"),
    path('register/', SignUpView.as_view(), name="register"),
    path('post/<int:pk>/delete/', login_required(BlogDeleteView.as_view()), name="delete_post"),
    path('post/<int:pk>/edit/', login_required(BlogUpdateView.as_view()), name="edit_post"),
    path('post/new/', login_required(BlogCreateView.as_view()), name="post_new"),
    path('post/<int:pk>/', BlogDetailView.as_view(), name="posts"),
    path('', BlogListView.as_view(), name="index")
]