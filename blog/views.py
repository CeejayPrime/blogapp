from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'index.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'posts.html'


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



