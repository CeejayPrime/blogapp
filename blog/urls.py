from django.urls import path
from . views import BlogListView, BlogDetailView


urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name="posts"),
    path('', BlogListView.as_view(), name="index")
]