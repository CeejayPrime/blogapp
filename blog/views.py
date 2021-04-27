from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm, CommentForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . models import Post, Comments


class BlogListView(ListView):
    model = Post
    template_name = 'index.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comments.objects.filter(post=self.get_object()).order_by('-pub_date')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comments(body=request.POST.get('body'),
                              name=self.request.user,
                              post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Post
    login_required = True
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']


@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Post
    login_required = True
    template_name = 'edit_post.html'
    fields = ['title', 'body']


@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    login_required = True
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'account/createuser.html'
    success_url = reverse_lazy('index')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


@unauthenticated_user
def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'account/login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')


# @method_decorator(login_required, name='dispatch')
# class UserView(DetailView):
#     model = Post
#     template_name = 'posts.html'


# class CommentView(CreateView):
#     model = Comments
#     template_name = 'comments.html'
#     fields = ['name', 'email', 'body']
#
#     def get_queryset(self):
#         return get_object_or_404(Post, category__slug=self.kwargs['category_slug'],
#                                  slug=self.kwargs['comment_slug'])


# def CommentView(request, slug):
#     template_name = 'post_detail.html'
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#
#     return render(request, template_name, {'post': post,
#                                            'comments': comments,
#                                            'new_comment': new_comment,
#                                            'comment_form': comment_form})





